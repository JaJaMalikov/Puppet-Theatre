#!/usr/bin/env python2

NightTint = {"id":1, "name":"Night Tint", "note":"",
"pages":[
	{"conditions":
		{"actorId":1, "actorValid":False, "itemId":1, "itemValid":False, "selfSwitchCh":"A", "selfSwitchValid":False, "switch1Id":1,
		"switch1Valid":False, "switch2Id":1, "switch2Valid":False, "variableId":1, "variableValid":False, "variableValue":0},
	"directionFix":False,
	"image":
		{"characterIndex":0, "characterName":"", "direction":2, "pattern":0, "tileId":0},
	"list":[
		{"code":223, "indent":0, "parameters":[[-68,-68,0,68],1,False]},
		{"code":0, "indent":0, "parameters":[]}
		],
	"moveFrequency":3,
	"moveRoute":{
		"list":[{ "code":0, "parameters":[]}],
		"repeat":True,
		"skippable":False,
		"wait":False},
	"moveSpeed":3,
	"moveType":0,
	"priorityType":0,
	"stepAnime":False,
	"through":False,
	"trigger":4,
	"walkAnime":True
}],
"x":0, "y":0}

Transfer = {"id":2, "name":"Transport","note":"",
"pages":[
	{"conditions":{
			"actorId":1,"actorValid":False,"itemId":1,"itemValid":False,"selfSwitchCh":"A","selfSwitchValid":False,"switch1Id":1,
			"switch1Valid":False,"switch2Id":1,"switch2Valid":False,"variableId":1,"variableValid":False,"variableValue":0},
		"directionFix":False,
		"image":
			{"characterIndex":0,"characterName":"","direction":2,"pattern":0,"tileId":0},
		"list":[
			#target = transfer["pages"][0]["list"][0]["parameters"][1=targetID, 2=x, 3=y]
			{"code":201,"indent":0,"parameters":[0,2,0,0,0,2]},
			{"code":0,"indent":0,"parameters":[]}
			],
		"moveFrequency":3,
		"moveRoute":{
			"list":[{ "code":0, "parameters":[]}],
			"repeat":True,
			"skippable":False,
			"wait":False},
		"moveSpeed":3,
		"moveType":0,
		"priorityType":0,
		"stepAnime":False,
		"through":False,
		"trigger":1,
		"walkAnime":True}
	],
	"x":0, 
	"y":0}

Image = {
	"id":171,
	"name":"EV171",
	"note":"",
	"pages":[
		{
			"conditions":{
				"actorId":1,
				"actorValid":False,
				"itemId":1,
				"itemValid":False,
				"selfSwitchCh":"A",
				"selfSwitchValid":False,
				"switch1Id":1,
				"switch1Valid":False,
				"switch2Id":1,
				"switch2Valid":False,
				"variableId":1,
				"variableValid":False,
				"variableValue":0
			},
		"directionFix":False,
		"image":{
			"characterIndex":0,
			"characterName":"",
			"direction":2,
			"pattern":0,
			"tileId":0
		},
		"list":[
			{
				"code":231,
				"indent":0,
				"parameters":[1,"",0,0,0,0,100,100,255,0]
			},
			{
				"code":0,
				"indent":0,
				"parameters":[]
			}
		],
		"moveFrequency":3,
		"moveRoute":{
			"list":[
				{
					"code":0,
					"parameters":[]
				}
			],
			"repeat":True,
			"skippable":False,
			"wait":False
		},
		"moveSpeed":3,
		"moveType":0,
		"priorityType":0,
		"stepAnime":False,
		"through":False,
		"trigger":4,
		"walkAnime":True}
	],
	"x":0,
	"y":0}