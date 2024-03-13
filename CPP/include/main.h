#pragma once

#include <Windows.h>
#include <iostream>
using namespace std;

enum class ConsoleColor {
	Clear,	// 原色
	White,	// 白色
	Red,	// 红色
	Green,	// 绿色
	Blue,	// 蓝色
	Yellow,	// 黄色
	Pink,	// 粉色
	Cyan	// 青色
};

static char SetConsoleColor(ConsoleColor color) {
	HANDLE hdl = GetStdHandle(STD_OUTPUT_HANDLE);
	switch (color) {
	case ConsoleColor::Clear:
		SetConsoleTextAttribute(hdl, FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED);
		break;
	case ConsoleColor::White:
		SetConsoleTextAttribute(hdl, FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED | FOREGROUND_INTENSITY);
		break;
	case ConsoleColor::Red:
		SetConsoleTextAttribute(hdl, FOREGROUND_RED | FOREGROUND_INTENSITY);
		break;
	case ConsoleColor::Green:
		SetConsoleTextAttribute(hdl, FOREGROUND_GREEN | FOREGROUND_INTENSITY);
		break;
	case ConsoleColor::Blue:
		SetConsoleTextAttribute(hdl, FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_INTENSITY);
		break;
	case ConsoleColor::Yellow:
		SetConsoleTextAttribute(hdl, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY);
		break;
	case ConsoleColor::Pink:
		SetConsoleTextAttribute(hdl, FOREGROUND_RED | FOREGROUND_BLUE | FOREGROUND_INTENSITY);
		break;
	case ConsoleColor::Cyan:
		SetConsoleTextAttribute(hdl, FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_INTENSITY);
		break;
	default:
		break;
	}
	return '\0';
}


static const vector<string> UtilsTypeString = {
	"exit            ",
	"rename          ",
	"epub_to_txt     ",
	"txt_to_txt      ",
	"txt_delete_space",
	"lrc_to_ass      ",
	"srt_to_ass      ",
};

static void CommandHelp() {
	SetConsoleColor(ConsoleColor::Yellow);
	printf("已实现的功能如下表: \n");

	for (int i = 0; i < UtilsTypeString.size(); i++) {
		SetConsoleColor(ConsoleColor::Red);
		printf("%s\t", UtilsTypeString[i].c_str());
		SetConsoleColor(ConsoleColor::White);
		printf(": ");

		switch (i) {
		case 0:
			printf("退出程序\n");
			break;
		case 1:
			printf("重命名文件: *.xxx => prefix_n.yyy\n");
			break;
		case 2:
			printf("将epub文件解压出来的HTML文件, 转化为TXT文件: *.html => *.txt\n");
			break;
		case 3:
			printf("将原本TXT文件中的xxx改为第xxx章, 转化为TXT文件: *.txt => *.txt\n");
			break;
		case 4:
			printf("将原本TXT文件中不规则的换行删除, 转化为TXT文件: *.txt => *.txt\n");
			break;
		case 5:
			printf("将LRC文件转化为ASS文件: *.lrc => *.ass\n");
			break;
		case 6:
			printf("将SRT文件转化为ASS文件: *.srt => *.ass\n");
			break;
		}
	}
	
	SetConsoleColor(ConsoleColor::Clear);
}