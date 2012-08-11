import sublime
import sublime_plugin
import copy
import re

class TokenStream:
	def __init__(self, src):
		#todo: true parsing
		return

class ViewInfo:
	def __init__(self):
		self.last_buffer_size = 0
		self.rbxutility_included = None

class LuaCompletions(sublime_plugin.EventListener):
	def __init__(self):
		try:
			self.token_stream = None
			self.do_enum_complete = None
			self.do_dot_complete = None
			self.do_colon_complete = None
			self.do_type_complete = None
			self.cancel_next_complete = False

			self.view_info = {}

			self.enums = {
				'FormFactor':  ['Brick', 'Plate', 'Custom', 'Symmetric'],
				'PartType':    ['Ball', 'Block', 'Cylinder'],
				'SurfaceType': ['Smooth', 'Hinge', 'Studs', 'Inlet', 'Weld', 'Unjoinable', 
				                'Motor', 'SteppingMotor', 'Universal', 'Glue'],
				'Material':    ['Concrete', 'CorrodedMetal', 'DiamondPlate', 'Foil', 'Grass',
				                'Ice', 'Plastic', 'Slate', 'Wood'],
				'Font':        ['Arial', 'ArialBold', 'Legacy'],
				'FontSize':    ['Size10', 'Size11', 'Size12', 'Size14', 'Size18', 'Size24',
				                'Size36', 'Size48', 'Size9', 'Size8'],
				'TextXAlignment': ['Center', 'Left', 'Right'],
				'TextYAlignment': ['Center', 'Top', 'Bottom'],
				'NormalId':    ['Back', 'Bottom', 'Front', 'Left', 'Right', 'Top'],
				'MeshType':    ['Brick', 'CornerWedge', 'Cylinder', 'FileMesh', 'Head', 'ParallelRamp',
				                'Prism', 'Pyramid', 'RightAngleRamp', 'Sphere', 'Torso', 'Wedge'],
				'FrameStyle':  ['RobloxRound', 'RobloxSquare', 'Custom', 'ChatBlue', 'ChatGreen', 'ChatRed'],
				'AnimationPriority': ['Idle', 'Movement', 'Action'],
			}
			self.known_props = {
				'FormFactor':  self.enums['FormFactor'],
				'Shape':       self.enums['PartType'],
				'BrickColor':  [
					('White', 'BrickColor.new(1)'),
					('Grey', 'BrickColor.new(2)'),
					('Light yellow', 'BrickColor.new(3)'),
					('Brick yellow', 'BrickColor.new(5)'),
					('Light green (Mint)', 'BrickColor.new(6)'),
					('Light reddish violet', 'BrickColor.new(9)'),
					('Pastel Blue', 'BrickColor.new(11)'),
					('Light orange brown', 'BrickColor.new(12)'),
					('Nougat', 'BrickColor.new(18)'),
					('Bright red', 'BrickColor.new(21)'),
					('Med. reddish violet', 'BrickColor.new(22)'),
					('Bright blue', 'BrickColor.new(23)'),
					('Bright yellow', 'BrickColor.new(24)'),
					('Earth orange', 'BrickColor.new(25)'),
					('Black', 'BrickColor.new(26)'),
					('Dark grey', 'BrickColor.new(27)'),
					('Dark green', 'BrickColor.new(28)'),
					('Medium green', 'BrickColor.new(29)'),
					('Lig. Yellowich orange', 'BrickColor.new(36)'),
					('Bright green', 'BrickColor.new(37)'),
					('Dark orange', 'BrickColor.new(38)'),
					('Light bluish violet', 'BrickColor.new(39)'),
					('Transparent', 'BrickColor.new(40)'),
					('Tr. Red', 'BrickColor.new(41)'),
					('Tr. Lg blue', 'BrickColor.new(42)'),
					('Tr. Blue', 'BrickColor.new(43)'),
					('Tr. Yellow', 'BrickColor.new(44)'),
					('Light blue', 'BrickColor.new(45)'),
					('Tr. Flu. Reddish orange', 'BrickColor.new(47)'),
					('Tr. Green', 'BrickColor.new(48)'),
					('Tr. Flu. Green', 'BrickColor.new(49)'),
					('Phosph. White', 'BrickColor.new(50)'),
					('Light red', 'BrickColor.new(100)'),
					('Medium red', 'BrickColor.new(101)'),
					('Medium blue', 'BrickColor.new(102)'),
					('Light grey', 'BrickColor.new(103)'),
					('Bright violet', 'BrickColor.new(104)'),
					('Br. yellowish orange', 'BrickColor.new(105)'),
					('Bright orange', 'BrickColor.new(106)'),
					('Bright bluish green', 'BrickColor.new(107)'),
					('Earth yellow', 'BrickColor.new(108)'),
					('Bright bluish violet', 'BrickColor.new(110)'),
					('Tr. Brown', 'BrickColor.new(111)'),
					('Medium bluish violet', 'BrickColor.new(112)'),
					('Tr. Medi. reddish violet', 'BrickColor.new(113)'),
					('Med. yellowish green', 'BrickColor.new(115)'),
					('Med. bluish green', 'BrickColor.new(116)'),
					('Light bluish green', 'BrickColor.new(118)'),
					('Br. yellowish green', 'BrickColor.new(119)'),
					('Lig. yellowish green', 'BrickColor.new(120)'),
					('Med. yellowish orange', 'BrickColor.new(121)'),
					('Br. reddish orange', 'BrickColor.new(123)'),
					('Bright reddish violet', 'BrickColor.new(124)'),
					('Light orange', 'BrickColor.new(125)'),
					('Tr. Bright bluish violet', 'BrickColor.new(126)'),
					('Gold', 'BrickColor.new(127)'),
					('Dark nougat', 'BrickColor.new(128)'),
					('Silver', 'BrickColor.new(131)'),
					('Neon orange', 'BrickColor.new(133)'),
					('Neon green', 'BrickColor.new(134)'),
					('Sand blue', 'BrickColor.new(135)'),
					('Sand violet', 'BrickColor.new(136)'),
					('Medium orange', 'BrickColor.new(137)'),
					('Sand yellow', 'BrickColor.new(138)'),
					('Earth blue', 'BrickColor.new(140)'),
					('Earth green', 'BrickColor.new(141)'),
					('Tr. Flu. Blue', 'BrickColor.new(143)'),
					('Sand blue metallic', 'BrickColor.new(145)'),
					('Sand violet metallic', 'BrickColor.new(146)'),
					('Sand yellow metallic', 'BrickColor.new(147)'),
					('Dark grey metallic', 'BrickColor.new(148)'),
					('Black metallic', 'BrickColor.new(149)'),
					('Light grey metallic', 'BrickColor.new(150)'),
					('Sand green', 'BrickColor.new(151)'),
					('Sand red', 'BrickColor.new(153)'),
					('Dark red', 'BrickColor.new(154)'),
					('Tr. Flu. Yellow', 'BrickColor.new(157)'),
					('Tr. Flu. Red', 'BrickColor.new(158)'),
					('Gun metallic', 'BrickColor.new(168)'),
					('Red flip/flop', 'BrickColor.new(176)'),
					('Yellow flip/flop', 'BrickColor.new(178)'),
					('Silver flip/flop', 'BrickColor.new(179)'),
					('Curry', 'BrickColor.new(180)'),
					('Fire Yellow', 'BrickColor.new(190)'),
					('Flame yellowish orange', 'BrickColor.new(191)'),
					('Reddish brown', 'BrickColor.new(192)'),
					('Flame reddish orange', 'BrickColor.new(193)'),
					('Royal blue', 'BrickColor.new(195)'),
					('Dark Royal blue', 'BrickColor.new(196)'),
					('Bright reddish lilac', 'BrickColor.new(198)'),
					('Dark stone grey', 'BrickColor.new(199)'),
					('Lemon metalic', 'BrickColor.new(200)'),
					('Light stone grey', 'BrickColor.new(208)'),
					('Dark Curry', 'BrickColor.new(209)'),
					('Faded green', 'BrickColor.new(210)'),
					('Turquoise', 'BrickColor.new(211)'),
					('Light Royal blue', 'BrickColor.new(212)'),
					('Medium Royal blue', 'BrickColor.new(213)'),
					('Rust', 'BrickColor.new(216)'),
					('Brown', 'BrickColor.new(217)'),
					('Reddish lilac', 'BrickColor.new(218)'),
					('Lilac', 'BrickColor.new(219)'),
					('Light lilac', 'BrickColor.new(220)'),
					('Bright purple', 'BrickColor.new(221)'),
					('Light purple', 'BrickColor.new(222)'),
					('Light pink', 'BrickColor.new(223)'),
					('Light brick yellow', 'BrickColor.new(224)'),
					('Warm yellowish orange', 'BrickColor.new(225)'),
					('Cool yellow', 'BrickColor.new(226)'),
					('Dove blue', 'BrickColor.new(232)'),
					('Medium lilac', 'BrickColor.new(268)'),
					('Institutional white', 'BrickColor.new(1001)'),
					('Mid gray', 'BrickColor.new(1002)'),
					('Really black', 'BrickColor.new(1003)'),
					('Really red', 'BrickColor.new(1004)'),
					('Deep orange', 'BrickColor.new(1005)'),
					('Alder', 'BrickColor.new(1006)'),
					('Dusty Rose', 'BrickColor.new(1007)'),
					('Olive', 'BrickColor.new(1008)'),
					('New Yeller', 'BrickColor.new(1009)'),
					('Really blue', 'BrickColor.new(1010)'),
					('Navy blue', 'BrickColor.new(1011)'),
					('Deep blue', 'BrickColor.new(1012)'),
					('Cyan', 'BrickColor.new(1013)'),
					('CGA brown', 'BrickColor.new(1014)'),
					('Magenta', 'BrickColor.new(1015)'),
					('Pink', 'BrickColor.new(1016)'),
					('Deep orange', 'BrickColor.new(1017)'),
					('Teal', 'BrickColor.new(1018)'),
					('Toothpaste', 'BrickColor.new(1019)'),
					('Lime green', 'BrickColor.new(1020)'),
					('Camo', 'BrickColor.new(1021)'),
					('Grime', 'BrickColor.new(1022)'),
					('Lavender', 'BrickColor.new(1023)'),
					('Pastel light blue', 'BrickColor.new(1024)'),
					('Pastel orange', 'BrickColor.new(1025)'),
					('Pastel violet', 'BrickColor.new(1026)'),
					('Pastel blue-green', 'BrickColor.new(1027)'),
					('Pastel green', 'BrickColor.new(1028)'),
					('Pastel yellow', 'BrickColor.new(1029)'),
					('Pastel brown', 'BrickColor.new(1030)'),
					('Royal purple', 'BrickColor.new(1031)'),
					('Hot pink', 'BrickColor.new(1032)'),
				],
				'TopSurface':    self.enums['SurfaceType'],
				'BottomSurface': self.enums['SurfaceType'],
				'RightSurface':  self.enums['SurfaceType'],
				'LeftSurface':   self.enums['SurfaceType'],
				'FrontSurface':  self.enums['SurfaceType'],
				'BackSurface':   self.enums['SurfaceType'],
				'Font':        self.enums['Font'],
				'FontSize':    self.enums['FontSize'],
				'TextXAlignment': self.enums['TextXAlignment'],
				'TextYAlignment': self.enums['TextYAlignment'],
				'MeshType':  self.enums['MeshType'],
				'Style':     self.enums['FrameStyle'],
				'Priority':  self.enums['AnimationPriority'],
			}

			#calculate enums
			for enum, values in self.enums.items():
				for i, v in enumerate(values):
					values[i] = (v, "'{0}'".format(v))

			#fix brickcolor
			try:
				for i, v in enumerate(self.known_props['BrickColor']):
					self.known_props['BrickColor'][i] = ("Color: {0}".format(v[0]), v[1])
			except Exception, e:
				print(e)


			#default globals
			self.default_completions = [
				#lua keywordl
				"if",
				"while",
				"repeat",
				"until",
				"then",
				"elseif",
				"else",
				"until",
				"do",
				"function",

				#glabals
				"game",
				"script",
				"Workspace",
				"Lighting",
				"Players",
				"Debris",

				#types
				"BasePart",
				"Script",
				"Model",
				"Part",
				"Frame",

				#atomics
				("newUDim2", "UDim2.new($1)"),
				("newVector3", "Vector3.new($1)"),
				("newRay", "Ray.new($1)"),
				("newRegion3", "Region3.new($1)"),
				("newRegion3int16", "Region3int16.new($1)"),
				("newColor3", "Color3.new($1)"),
				("newBrickColor", "BrickColor.new($1)"),
				("newRay", "Ray.new($1)"),
				("newInstance", "Instance.new('$1')"),
			]

			self.type_completions = [
				("physical", "Part"),
				("physical", "BasePart"),
				#
				("grahical", "SpecialMesh"),
				("grahical", "BlockMesh"),
				("graphical", "Smoke"),
				("graphical", "Fire"),
				#
				"Tool",
				"Script",
				"LocalScript",
				#
				("effector", "BodyPosition"),
				("effector", "BodyGyro"),
				("effector", "BodyAngularVelocity"),
				("effector", "BodyForce"),
				("effector", "BodyVelocity"),
				#
				("gui", "TextButton"),
				("gui", "TextLabel"),
				("gui", "Frame"),
				("gui", "TextBox"),
				("gui", "ImageButton"),
				("gui", "ImageLabel"),
				("gui", "ScreenGui"),
				("gui", "BillboardGui"),
			]
			for i, v in enumerate(self.type_completions):
				if not (type(v) is tuple): 
					self.type_completions[i] = ('other '+v, v)
				else:
					self.type_completions[i] = (v[0]+' '+v[1], v[1])

			self.method_completions = [
				#methods
				("FindFirstChild", "FindFirstChild('$1')"),
				("GetChildren", "GetChildren()"),
				("IsA", "IsA('$1')"),
				("Clone", "Clone()"),
				("GetFullName", "GetFullName()"),
				("IsAncestorOf", "IsAncestorOf($1)"),
				("IsDescendantOf", "IsDescendantOf($1)"),
				("Destroy", "Destroy()"),
				("ClearAllChildren", "ClearAllChildren()"),
				("GetMass", "GetMass()"),
				("FindPartOnRay", "FindPartOnRay($1)"),
				("FindPartOnRayWithIgnoreList", "FindPartOnRayWithIgnoreList($1)"),
				("TakeDamage", "TakeDamage($1)"),
				("Destroy", "Destroy()"),
				("AddItem", "AddItem($1)"),
			]

			self.prop_completions = [
				#properties
				"Name",
				"Parent",
				"ClassName",
				"Value",
				"Archivable",
				"Anchored",
				"Locked",
				"CanCollide",
				"Character",
				"Humanoid",
				"CFrame",
				"Position",
				"Velocity",
				"magnitude",
				"UnitRay",
				"Target",
				"Icon",
				"Health",
				"MaxHealth",
				"TeamColor",
				"Size",
				"Enabled",
				"Disabled",
				"Color",
				"BrickColor",
				"Transparency",
				"BackgroundTransparency",
				"TextTransparency",
				"TextStrokeTransparency",
				"TextColor3",
				"TextStrokeColor3",
				"SizeConstraint",
				"TextFits",
				"TextScaled",
				"Visible",
				"ZIndex",
				"TextWrapped",
				"Text",
				"MultiLine",
				"ClipsDescendants",
				"ClearTextOnFocus",
				"BorderSizePixel",
				"BorderColor3",
				"BackgroundColor3",
				"Active",
				"AbsoluteSize",
				"AbsolutePosition",
				"MeshId",
				"MeshType",
				"FormFactor",
				"Scale",
				"TextureId",
				"AnimationId",
				"VertexColor",
				"Color",
				"Heat",
				"SecondaryColor",
				"Adornee",
				"StudsOffset",
				"AlwaysOnTop",
				"ExtentsOffset",
				"SizeOffset",
				"PlayerToHideFrom",


				#events
				("ChildAdded event", "ChildAdded:connect(function(child)\n\t$1\nend)"),
				("ChildRemoved event", "ChildRemoved:connect(function(child)\n\t$1\nend)"),
				("Changed event", "Changed:connect(function(property)\n\t$1\nend"),
				("Touched event", "Touched:connect(function(property)\n\t$1\nend"),	
				("Died event", "Died:connect(function()\n\t$1\nend"),		
				("Button1Down event", "Button1Down:connect(function()\n\t$1\nend"),
				("Button1Up event", "Button1Up:connect(function()\n\t$1\nend"),
				("Move event", "Move:connect(function()\n\t$1\nend"),
				("WheelForward event", "WheelForward:connect(function()\n\t$1\nend"),
				("WheelBack event", "WheelBack:connect(function()\n\t$1\nend"),
				("MouseButton1Down event", "MouseButton1Down:connect(function(x, y)\n\t$1\nend"),
				("MouseButton1Up event", "MouseButton1Up:connect(function(x, y)\n\t$1\nend"),
				("MouseButton1Click event", "MouseButton1Click:connect(function()\n\t$1\nend"),
				("MouseEnter event", "MouseEnter:connect(function(x, y)\n\t$1\nend"),
				("MouseLeave event", "MouseLeave:connect(function(x, y)\n\t$1\nend"),
				("MouseMoved event", "MouseMoved:connect(function(x, y)\n\t$1\nend"),
			]

			self.requires_assetid = set([
				"MeshId",
				"TextureId",
				"Texture",
				"SoundId",
				"AnimationId",
				"Icon",
			])

			for i, v in enumerate(self.default_completions):
				if not (type(v) is tuple):
					self.default_completions[i] = (v, v)

			for i, v in enumerate(self.prop_completions):
				if not (type(v) is tuple):
					self.prop_completions[i] = (v, v)

			return
		except Exception, e:
			sublime.status_message("Problem: {0}".format(e)) 


	def get_info(self, view):
		info = self.view_info.get(view.id())
		if not info:
			info = ViewInfo()
			self.view_info[view.id()] = info
		return info 


	def ParseLua(self, src):
		self.tokens = TokenStream(src)


	def on_modified(self, view):
		info = self.get_info(view)

		filename = view.file_name()
		if not filename or not filename.endswith('.lua'):
			return

		if info.rbxutility_included == None:
			whole_text = view.substr(sublime.Region(0, view.size()))
			match = re.search(r"""LoadLibrary\(?('|")RbxUtility('|")\)?""", whole_text)
			if match:
				info.rbxutility_included = True
			else:
				needs_rbxutility = re.search(r"""Create('|")\w+('|")|CreateSignal\(""", whole_text)
				if needs_rbxutility:
					info.rbxutility_included = True
					edit = view.begin_edit("automatic_loadlibrary_inculde", "rbxutility")
					view.insert(edit, 0, """local RbxUtility = LoadLibrary('RbxUtility')\n"""
					                     """local Create = RbxUtility.Create\n"""
					                     """local CreateSignal = RbxUtility.CreateSignal\n""")
					view.end_edit(edit)
				else:
					info.rbxutility_included = False

		newSize = view.size()
		oldSize = info.last_buffer_size
		info.last_buffer_size = newSize
		if newSize <= oldSize: 
			return

		sel = view.sel()  
		if len(sel) > 0:
			cursorPos = sel[0].b
			lineStart = view.line(cursorPos).a
			toLeft = view.substr(sublime.Region(lineStart, cursorPos))
			sublime.status_message("Sel: {0}".format(toLeft))
			if len(toLeft) > 0 and toLeft[-1] == '.':
				self.do_dot_complete = True
				view.run_command('auto_complete')

			elif len(toLeft) > 0 and toLeft[-1] == ':': 
				self.do_colon_complete = True
				view.run_command('auto_complete')

			elif info.rbxutility_included == False and re.search(r"""Create('|")\w+('|")|CreateSignal\(""", toLeft):
				#require rbxutility
				info.rbxutility_included = True
				edit = view.begin_edit("automatic_loadlibrary_inculde", "rbxutility")
				view.insert(edit, 0, """local RbxUtility = LoadLibrary('RbxUtility')\n"""
				                     """local Create = RbxUtility.Create\n"""
				                     """local CreateSignal = RbxUtility.CreateSignal\n""")
				view.end_edit(edit)				

			else:
				#match known property assignment
				wordAssignMatch = re.search(r"""(\w+)\s*= $""", toLeft)
				if wordAssignMatch:
					word = wordAssignMatch.group(1)
					if self.known_props.get(word, None):
						self.do_enum_complete = word
						view.run_command('auto_complete')
				else:
					#match assetids
					assetMatch = re.search(r"""(\w+)\s*=\s*(\d+)[^\d]""", toLeft)
					if assetMatch:
						if assetMatch.group(1) in self.requires_assetid:
							assetid = assetMatch.group(2)
							replace_at = lineStart + assetMatch.start(2)
							replace_len = len(assetid)
							edit = view.begin_edit("automatic_assetid_replacement")
							view.replace(edit, sublime.Region(replace_at, replace_at+replace_len),
							             "'http://www.roblox.com/asset/?id={0}'".format(assetid))
							view.end_edit(edit)
					else:
						#match foreach loops
						foreachMatch = re.search(r"""foreach\s*(.*?)\s*do""", toLeft)
						if foreachMatch:
							self.cancel_next_complete = True
							replace_at = lineStart + foreachMatch.start(0)
							replace_len = len(foreachMatch.group(0))
							replacement = foreachMatch.group(1)
							replacement_text = "for _, child in pairs({0}:GetChildren()) do\n\nend\n".format(replacement)
							edit = view.begin_edit("foreach_replacement")
							view.replace(edit, sublime.Region(replace_at, replace_at+replace_len),
							             replacement_text)
							view.end_edit(edit)
							view.sel().clear()
							view.sel().add(sublime.Region(replace_at+len(replacement_text)-5,
							                              replace_at+len(replacement_text)-5))
						else:
							#match typing IsA, Create or Instance.new argument
							typeArgMatch = re.search(r"""(IsA|Instance\.new|Create)\(?('|")$""", toLeft)
							if typeArgMatch:
								self.do_type_complete = True
								view.run_command('auto_complete')



	def on_query_completions(self, view, prefix, locations):
		info = self.get_info(view)

		filename = view.file_name()
		if not filename or not filename.endswith('.lua'):
			return

		if self.cancel_next_complete:
			self.cancel_next_complete = False
			return

		if self.do_enum_complete:
			word = self.do_enum_complete
			self.do_enum_complete = None
			#
			values = self.known_props.get(word, None)
			if values:
				complete = copy.copy(values)
				complete.append(('--------',''))
				for v in self.default_completions:
					complete.append(v)
				return complete

		elif self.do_dot_complete:
			self.do_dot_complete = None
			#
			complete = copy.copy(self.prop_completions)
			complete.append(('---------',''))
			for v in self.default_completions:
				complete.append(v)
			return complete

		elif self.do_colon_complete:
			self.do_colon_complete = None
			#
			complete = copy.copy(self.method_completions)
			complete.append(('--------',''))
			return complete

		elif self.do_type_complete:
			self.do_type_complete = None
			#
			complete = copy.copy(self.type_completions)
			complete.append(('---------',''))
			return complete

		complete = copy.copy(self.default_completions)
		for v in self.prop_completions:
			complete.append(v)
		return complete
