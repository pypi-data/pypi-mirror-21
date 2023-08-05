#! python3

import hashlib
from itertools import cycle
import json
import re
import string
import threading
import traceback
from os.path import join as path_join, split as path_split, splitext

from worker import sleep, WorkerExit
from requests.utils import dict_from_cookiejar

from ..safeprint import print
from ..error import (
	ModuleError, PauseDownloadError, LastPageError, SkipEpisodeError, is_http
)
from ..io import content_write, content_read, path_each
from ..channel import download_ch, mission_ch
from ..config import setting
from ..profile import get as profile

from .grabber import grabhtml, grabimg

mission_lock = threading.Lock()

def debug_log(*args):
	if setting.getboolean("errorlog"):
		content_write(profile("debug.log"), ", ".join(args) + "\n", append=True)

class Mission:
	"""Create Mission object. Contains information of the mission."""

	def __init__(self, title=None, url=None, episodes=None, state="INIT"):
		"""Construct."""
		from ..mods import get_module

		super().__init__()

		self.title = title
		self.url = url
		self.episodes = episodes
		self.state = state
		self.module = get_module(url)
		if not self.module:
			raise ModuleError("Get module failed!")
			
class MissionProxy:
	"""Publish MISSION_PROPERTY_CHANGED event when property changed"""
	def __init__(self, mission):
		self.__dict__["mission"] = mission

	def __getattr__(self, name):
		return getattr(self.mission, name)

	def __setattr__(self, name, value):
		with mission_lock:
			setattr(self.mission, name, value)
		mission_ch.pub("MISSION_PROPERTY_CHANGED", self)

	def tojson(self):
		json = vars(self.mission).copy()
		del json["module"]
		return json
		
class Image:
	"""Image container"""
	def __init__(self, url=None, get_url=None, data=None, filename=None):
		self.url = url
		self.get_url = get_url
		self.data = data
		self.filename = filename
		self.static_filename = bool(filename)
		
		if not filename and url:
			self.filename = url_extract_filename(url)
			
	def resolve(self):
		if not self.url and self.get_url:
			self.url = self.get_url()
		
		if not self.filename and self.url:
			self.filename = url_extract_filename(self.url)
	
	@classmethod
	def create(cls, data):
		if isinstance(data, Image):
			return data
			
		if isinstance(data, str):
			return Image(url=data)
			
		if callable(data):
			return Image(get_url=data)
			
		return Image(data=data)
		
def url_extract_filename(url):
	filename = url.rpartition("/")[2]
	filename = re.sub(r"\.\w{3,4}$", "", filename)
	return filename
		
def create_mission(url):
	return MissionProxy(Mission(url=url))

class Episode:
	"""Create Episode object. Contains information of an episode."""

	def __init__(self, title=None, url=None, current_url=None, current_page=0,
			skip=False, complete=False, total=0, image=None):
		"""Construct."""
		self.title = title
		self.url = url
		self.current_url = current_url
		# position of images on current page
		self.current_page = current_page
		self.skip = skip
		self.complete = complete
		# total number of images in this episode
		self.total = total
		self.image = image

def format_escape(s):
	"""Escape {} to {{}}"""
	return re.sub("([{}])", r"\1\1", s)
	
VALID_FILE_TYPES = (
	# images
	".jpg", ".jpeg", ".gif", ".png", ".svg", ".psd", ".webp",
	# zips
	".zip", ".rar",
	# videos
	".mp4", ".mkv", ".swf", ".webm",
	# json
	".json"
)

def create_safefilepath_table():
	table = {}
	table.update({
		"/": "／",
		"\\": "＼",
		"?": "？",
		"|": "｜",
		"<": "＜",
		">": "＞",
		":": "：",
		"\"": "＂",
		"*": "＊"
	})
	table.update({
		c: None for c in set([chr(i) for i in range(128)]).difference(string.printable)
	})
	return str.maketrans(table)
	
safefilepath_table = create_safefilepath_table()

def safefilepath(s):
	"""Return a safe directory name."""
	return s.strip().translate(safefilepath_table)

def download(mission, savepath):
	"""Download mission to savepath."""

	# warning there is a deadlock,
	# never do mission.lock.acquire in callback...
	print("Start downloading " + mission.title)
	mission.state = "DOWNLOADING"
	try:
		crawl(mission, savepath)

		# Check if mission is complete
		for ep in mission.episodes:
			if not ep.complete and not ep.skip:
				raise Exception("Mission is not completed")

	except WorkerExit:
		mission.state = "PAUSE"
		download_ch.pub('DOWNLOAD_PAUSE', mission)
		raise

	except PauseDownloadError as err:
		mission.state = "ERROR"
		download_ch.pub('DOWNLOAD_INVALID', (err, mission))

	except Exception as err:
		mission.state = "ERROR"
		download_ch.pub('DOWNLOAD_ERROR', (err, mission))
		raise

	else:
		mission.state = "FINISHED"
		download_ch.pub("DOWNLOAD_FINISHED", mission)	
	
def crawl(mission, savepath):
	"""Crawl each episode."""
	
	print("total {} episode.".format(len(mission.episodes)))

	for ep in mission.episodes:
		if ep.skip or ep.complete:
			continue

		print("Downloading ep {}".format(ep.title))
		
		try:
			crawler = Crawler(mission, ep, savepath)
			crawlpage(crawler)

		except LastPageError:
			print("Episode download complete!")
			ep.complete = True
			download_ch.pub("DOWNLOAD_EP_COMPLETE", (mission, ep))

		except SkipEpisodeError as err:
			print("Something bad happened, skip the episode.")
			if err.always:
				ep.skip = True

def get_checksum(b):
	return hashlib.md5(b).hexdigest() # nosec

def get_file_checksum(file):
	return get_checksum(content_read(file, raw=True))

class Downloader:
	"""Bind grabber with module's header, cookie..."""
	def __init__(self, mod):
		self.mod = mod
		
	def html(self, url, **kwargs):
		return grabhtml(
			url,
			header=self.get_header(),
			cookie=self.get_cookie(),
			done=self.handle_grab,
			**kwargs
		)
	
	def img(self, url, **kwargs):
		return grabimg(
			url,
			header=self.get_header(),
			cookie=self.get_cookie(),
			done=self.handle_grab,
			**kwargs
		)
		
	def get_header(self):
		"""Return downloader header."""
		return getattr(self.mod, "header", None)

	def get_cookie(self):
		"""Return downloader cookie."""
		cookie = getattr(self.mod, "cookie", {})
		config = getattr(self.mod, "config", {})
		
		for key, value in config.items():
			if key.startswith("cookie_"):
				name = key[7:]
				cookie[name] = value
				
		return cookie
		
	def handle_grab(self, session, _response):
		cookie = dict_from_cookiejar(session.cookies)
		config = getattr(self.mod, "config", None)
		if not config:
			return
			
		for key in config:
			if key.startswith("cookie_"):
				name = key[7:]
				if name in cookie:
					config[key] = cookie[name]

class SavePath:
	def __init__(self, root, mission, ep, escape=safefilepath):
		self.root = root
		self.mission_title = escape(mission.title)
		self.ep_title = escape(ep.title)
		self.noepfolder = getattr(mission.module, "noepfolder", False)
		self.files = None
		self.escape = escape
		
	def parent(self):
		if self.noepfolder:
			return path_join(self.root, self.mission_title)
		return path_join(self.root, self.mission_title, self.ep_title)
		
	def filename(self, page, ext=""):
		"""Build filename with page and ext"""
		if not isinstance(page, str):
			page = "{:03d}".format(page)
			
		page = self.escape(page)
			
		if self.noepfolder:
			return "{ep_title}_{page}{ext}".format(
				ep_title=self.ep_title,
				page=page,
				ext=ext
			)
		return "{page}{ext}".format(
			page=page,
			ext=ext
		)
		
	def full_fn(self, page, ext=""):
		"""Build full filename with page and ext"""
		return path_join(self.parent(), self.filename(page, ext))

	def exists(self, page):
		"""Check if current page exists in savepath."""
		if page is None:
			return False
		
		# FIXME: if multiple SavePath is created and sharing same .parent(), 
		# they should share the .files too.
		if self.files is None:
		
			self.files = {}
			
			def build_file_table(file):
				_dir, name = path_split(file)
				base, ext = splitext(name)
				self.files[base] = ext
				
			path_each(
				self.parent(),
				build_file_table
			)
			
		return self.files.get(self.filename(page))

class Crawler:
	"""Create Crawler object. Contains img url, next page url."""
	def __init__(self, mission, ep, savepath):
		"""Construct."""
		self.mission = mission
		self.ep = ep
		self.savepath = SavePath(savepath, mission, ep)
		self.mod = mission.module
		self.downloader = Downloader(mission.module)
		self.checksums = None
		self.is_init = False
		self.html = None
		self.image = None
		self.images = None
		self.image_bin = None
		self.image_ext = None
		self.filename = None
		
	def init(self):
		if not self.ep.current_url:
			self.ep.current_url = self.ep.url
		if not self.ep.current_page:
			self.ep.current_page = 1
			
		self.init_images(self.ep.current_page - 1)
			
		self.is_init = True
		
	def init_images(self, skip_pages=0):
		"""Grab html, images and move cursor to correct image by skip_pages"""
		self.get_html()
		self.get_images()
		
		try:
			# skip some images
			for _ in range(0, skip_pages):
				next(self.images)
			# get current image
			self.image = Image.create(next(self.images))
		except StopIteration:
			self.image = None
			
	def get_filename(self):
		if self.mission.module.config.getboolean("originalfilename"):
			return self.image.filename
		return self.ep.total + 1
		
	def page_exists(self):
		return self.savepath.exists(self.get_filename())
			
	def download_image(self):
		"""Download image"""
		if self.image.url:
			result = self.downloader.img(
				self.image.url, referer=self.ep.current_url)
				
			# redirected and url changed
			if result.response.history and not self.image.static_filename:
				self.image.filename = url_extract_filename(result.response.url)
			bin = result.bin
			ext = result.ext
		else:
			bin = json.dumps(self.image.data, indent="\t").encode("utf-8")
			ext = ".json"
			
		if not ext:
			raise Exception("Can't determine file type.")
			
		if ext not in VALID_FILE_TYPES:
			raise Exception("Bad file type: " + ext)
			
		self.image_bin = bin
		self.image_ext = ext
			
	def handle_image(self):
		"""Post processing"""
		if hasattr(self.mod, "imagehandler"):
			self.image_ext, self.image_bin = self.mod.imagehandler(
				self.image_ext, self.image_bin)

	def save_image(self):
		"""Write image to save path"""
		if getattr(self.mod, "circular", False):
			if not self.checksums:
				self.checksums = set()
				path_each(
					self.savepath,
					lambda file: self.checksums.add(get_file_checksum(file))
				)

			checksum = get_checksum(self.image_bin)
			if checksum in self.checksums:
				raise LastPageError
			else:
				self.checksums.add(checksum)
				
		try:
			content_write(self.savepath.full_fn(self.get_filename(), self.image_ext), self.image_bin)
		except OSError:
			traceback.print_exc()
			raise PauseDownloadError("Failed to write file!")

	def next_page(self):
		"""Iter to next page."""
		next_page = self.get_next_page()
		if not next_page:
			raise LastPageError
			
		self.ep.current_url = next_page
		self.ep.current_page = 1
		
		self.init_images()

	def next_image(self):
		self.ep.current_page += 1
		self.ep.total += 1
		try:
			self.image = Image.create(next(self.images))
		except StopIteration:
			self.image = None
			
	def resolve_image(self):
		self.image.resolve()
		
	def rest(self):
		"""Rest some time."""
		sleep(getattr(self.mod, "rest", 0))
		
	def get_next_page(self):
		if (hasattr(self.mod, "get_next_page") 
				and isinstance(self.html, str)):
			# self.html is not a str if self.ep.image is not None
			return self.mod.get_next_page(
				self.html,
				self.ep.current_url
			)
		
	def get_html(self):
		if self.ep.image:
			self.html = True
		else:
			self.html = self.downloader.html(self.ep.current_url)
		
	def get_images(self):
		"""Get images"""
		if self.ep.image:
			images = self.ep.image
		else:
			images = self.mod.get_images(
				self.html,
				self.ep.current_url
			)
		if isinstance(images, str):
			images = [images]
		try:
			self.images = iter(images)
		except TypeError:
			self.images = iter([images])
		
	def handle_error(self, error):
		"""Send error to error handler."""
		handler = getattr(self.mod, "errorhandler", None)
		if not handler:
			return

		try:
			handler(error, self)

		except Exception as err: # pylint: disable=broad-except
			print("[Crawler] Failed to handle error: {}".format(err))
			
			
def crawlpage(crawler):
	"""Crawl all pages of an episode.

	To complete current episode, raise LastPageError.
	To skip current episode, raise SkipEpisodeError.
	To stop downloading (fatal error), raise PauseDownloadError.
	"""
	
	def download():
		if not crawler.is_init:
			debug_log("D_INIT")
			crawler.init()
			
		if not crawler.html:
			debug_log("D_INIT_IMAGE")
			crawler.init_images()
	
		if not crawler.image:
			debug_log("D_NEXT_PAGE")
			crawler.next_page()
			return
			
		if crawler.page_exists():
			debug_log("D_NEXT_IMAGE")
			print("page {} already exist".format(crawler.ep.total + 1))
			crawler.next_image()
			return
			
		debug_log("D_RESOLVE")
		crawler.resolve_image()
		print("Downloading {} page {}: {}\n".format(
			crawler.ep.title, crawler.ep.total + 1, crawler.image.url))
		debug_log("D_DOWNLOAD")
		crawler.download_image()
		debug_log("D_HANDLE")
		crawler.handle_image()
		debug_log("D_SAVE")
		crawler.save_image()
		debug_log("D_PUB")
		mission_ch.pub("MISSION_PROPERTY_CHANGED", crawler.mission)
		debug_log("D_REST")
		crawler.rest()
		debug_log("D_NEXT_IMAGE")
		crawler.next_image()

	def download_error(er):
		if is_http(er, code=429):
			# retry doesn't work with 429 error
			sleep(5)
			raise er
		else:
			crawler.handle_error(er)
			sleep(5)

	error_loop(download, download_error)

def error_loop(process, handle_error=None, limit=10):
	"""Loop process until error. Has handle error limit."""
	errorcount = 0
	while True:
		try:
			process()
		except Exception as er: # pylint: disable=broad-except
			traceback.print_exc()
			errorcount += 1
			if errorcount >= limit:
				raise SkipEpisodeError(always=False)
			if handle_error:
				handle_error(er)
		# except ExitErrorLoop:
			# break
		else:
			errorcount = 0

def analyze(mission):
	"""Analyze mission."""
	try:
		Analyzer(mission).analyze()

	except WorkerExit:
		mission.state = "ERROR"
		raise

	except Exception as err: # pylint: disable=broad-except
		mission.state = "ERROR"
		traceback.print_exc()
		download_ch.pub("ANALYZE_FAILED", (err, mission))

	except PauseDownloadError as err:
		mission.state = "ERROR"
		download_ch.pub("ANALYZE_INVALID", (err, mission))

	else:
		download_ch.pub("ANALYZE_FINISHED", mission)

def remove_duplicate_episode(mission):
	"""Remove duplicate episodes."""
	s = set()
	s2 = set()
	result = []
	for ep in mission.episodes:
		if ep.url not in s and ep.title not in s2:
			s.add(ep.url)
			s2.add(ep.title)
			result.append(ep)
	mission.episodes = result
	
class Analyzer:
	"""Analyze mission"""
	def __init__(self, mission):
		self.mission = mission
		self.downloader = Downloader(mission.module)
		self.old_urls = None
		self.old_titles = None
		self.is_new = not mission.episodes
		self.html = None
		
	def analyze(self):
		"""Start analyze"""
		print("Start analyzing {}".format(self.mission.url))

		self.mission.state = "ANALYZING"
		
		# one-time mission
		if self.is_onetime():
			ep = self.mission.episodes[0]
			if ep.skip or ep.complete:
				self.mission.state = "FINISHED"
			else:
				self.mission.state = "UPDATE"
			print("Analyzing success!")
			return
			
		self.html = self.downloader.html(self.mission.url, raise_429=False)
		
		if not self.mission.title:
			self.mission.title = self.mission.module.get_title(
				self.html, self.mission.url)
				
		self.analyze_pages()
				
		if self.is_new:
			self.mission.state = "ANALYZED"
			
		elif all(e.complete or e.skip for e in self.mission.episodes):
			self.mission.state = "FINISHED"
			
		else:
			self.mission.state = "UPDATE"

		print("Analyzing success!")
		
	def analyze_pages(self):
		"""Crawl for each pages"""
		url = self.mission.url
		new_eps = []
		
		while True:
			eps = self.mission.module.get_episodes(self.html, url)
			self.transform_title(eps)
			
			# add result episodes into new_eps
			duplicate = False
			for ep in reversed(eps):
				if self.contains(ep):
					duplicate = True
					continue
				new_eps.append(ep)
				self.add(ep)
				
			if (len(new_eps) == 1 and new_eps[0].url == self.mission.url or
					duplicate):
				break
				
			# get next page
			next_url = self.get_next_page(self.html, url)
			if not next_url:
				break
			url = next_url
			print('Analyzing {}...'.format(url))
			self.html = self.downloader.html(url, raise_429=False)
			
		if not self.mission.episodes:
			self.mission.episodes = []
		self.mission.episodes.extend(reversed(new_eps))
		
		if not self.mission.episodes:
			raise Exception("Episode list is empty")
		
	def get_next_page(self, html, url):
		if not hasattr(self.mission.module, "get_next_page"):
			return None
		return self.mission.module.get_next_page(html, url)

	def contains(self, ep):
		"""Check if mission contains episode"""
		self.build_cache()
		return ep.url in self.old_urls or ep.title in self.old_titles
		
	def add(self, ep):
		"""Add episode to cache"""
		self.build_cache()
		self.old_urls.add(ep.url)
		self.old_titles.add(ep.title)
		
	def build_cache(self):
		"""Build episode set for existence test"""
		if self.old_urls is None:
			self.old_urls = set()
			if self.mission.episodes:
				self.old_urls.update(e.url for e in self.mission.episodes)
		if self.old_titles is None:
			self.old_titles = set()
			if self.mission.episodes:
				self.old_titles.update(e.title for e in self.mission.episodes)
			
	def transform_title(self, eps):
		format = self.mission.module.config.get("titlenumberformat")
		if not format:
			return
		for ep in eps:
			# ignore mission title if exists
			title = list(ep.title.partition(self.mission.title))
			for i in (0, 2):
				title[i] = format_number(title[i], format)
			ep.title = "".join(title)
			
	def is_onetime(self):
		"""Check if the mission should only be analyze once"""
		return (self.mission.episodes and
			self.mission.episodes[0].url == self.mission.url)

def format_number(title, format):
	"""第3卷 --> 第003卷"""
	def replacer(match):
		number = match.group()
		return format.format(int(number))
	return re.sub(r"\d+", replacer, title)

class CycleList:
	"""Create a cycled list"""
	def __init__(self, list):
		self.list = cycle(list)
		self.item = None
		self.next()
		
	def next(self):
		"""Move to next item"""
		self.item = next(self.list)
		
	def get(self):
		"""Get current item"""
		return self.item
	