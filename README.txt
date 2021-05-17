

Outline of future releases:

###################################################changes#################################
1 - turn help menus into a single function X
3 - move imagelist menus to imagelist - object_ctrl, image_list X
4 - move objectlist menus to object_list - object_ctrl, object_list X
21- turn all state_ctrl sub functions into menu options for keyboard shortcuts - pos_panel, rot_panel, scale_panel 
	abandoned because the shortcuts would be too numerous

2 - remove load check OBJ2D

12- #sampler turned into object to retain audio waveform data - timeline_ctrl, sampler
13- #remove slider and upgrade pygamepanel to act as timeline slider - timeline_ctrl
14- #remove full resize event from pygamepanel, make it larger than it needs to be only resize waveform - timeline_ctrl
15- ?upgrade pygamepanel to act more like a pygame window with extra functionality - pygame_panel

22- add undo/redo feature, any time self.data is written to, copy.deepcopy to rolling list, add one to flow_control variable
	undo moves flow_control variable back one, redo adds one, doesn't change if index = 0 or len(list)
		changes made check if the current flow_control is at end of list, if not it truncates the list - whole project

23- unlimited object composition, post modern opengl

8 - add keystroke listener to render_ctrl, add key binds - render_ctrl
9 - adjust on_mouse_down for general purpose use, use resize viewbox- render_ctrl

5 - delete object should ask "are you sure" - object_list (also added to overwrite functions)
7 - check if update_object is needed - object_ctrl (yes it is)
24- add limited object composition - object_ctrl (very limited but it works!)

25- #turn render panel into notebook, second page controls the current state of the render window
10- #merge render frames and render to video - render_video_dialog, render_frames_dialog
27- #renders to multiple resolutions
11- ?add feedback and statusbar of ffmpeg render - render_video_dialog
26- #render output compatible with #youtube and Xtwitter

16- turn state_ctrl into notebook - state_ctrl
17- add overwrite panel to position panel - state_ctrl, pos_panel
18- add overwrite panel to rotation panel - state_ctrl, rot_panel
19- add overwrite panel to scale panel - state_ctrl, scale_panel
20- add flip panel to scale panel - state_ctrl, scale_panel

#########################################finished changes################################################

28- heirarchical drawing proccess:
	list all parents:
		parent.draw():  <-----------|
			self.transform()        |
			for child in children:  |
				child.draw() -------|



used shortcuts: N, O, S, A, X, shft+S, I, L, U, J, G, H, Z, Y

Beta:
    number	nickname					change
-------------------------------------------------------------------------------------
[X] 1.0.0 - "Better than Nothing"		Functional, bare bones
[X] 1.0.1 - 							Code refactored, commented, and made maintainable
[X] 1.1.0 - "Family Sticks Together"	5, 6, 7, 24, Basic Composite objects added, parent/child relationship
[X] 1.2.0 - "Record me Daddy"			8, 9, add keybinds and fix mouse down, render_ctrl
[X] 1.2.1 - 							1, 3, 4, 21,  Menu Overhaul
[X] 1.3.0 - "The Time Machine"			22, Add undo/redo
[X] 1.4.0 - "Soul Window"				12-15, Upgrade pygame panel to act as timeline control
[X] 1.5.0 -	"Ultimate Porpoise"			10, 11, 25, 26, 27, render video overhaul
[X] 1.6.0 - "State of the Union"		16, 17, 18, 19, 20, state_ctrl overhaul
[X]	1.6.2 - 							bug fixes, general tidying of functions
[X] 1.7.0 - "Soylent Peen"				28, added composite objects, saving and loading
[X] 1.7.1 - 							Changing the point of origin of objects
[X] 1.7.2 - 							Add point of origin state control
[X] 1.7.3 - 							Repair stacked drawing and transparency issues
[X] 1.8.0 - 							fix history memory issues
[X] 1.8.1 - 							reverted edit history
[ ] 1.8.5 - 							

[ ] 2.0.0 - "FuuuuuTuuuuure"			Migrate to modern opengl
[X] 2.0.1 - 							Code refactored, commented, and made maintainable
[X]	2.1.0 - 							23, Adding complex composite objects, full lineage using transformation hierarchy

[ ] 3.0.0 - "I C what you did there"	Migrate to C++
[ ] 3.0.1 - 							Code refactored, commented, and made maintainable