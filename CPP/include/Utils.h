#pragma once
#include "../include/EPUB_TO_TXT.h"
#include "../include/TXT_TO_TXT.h"
#include "../include/TXT_TO_TXT_Delete_Space.h"
#include "../include/LRC_TO_ASS.h"
#include "../include/SRT_TO_ASS.h"
#include <string>
#include <vector>
using namespace std;

enum class UtilsType {
	NONE,
	RENAME,						// 重命名文件
	EPUB_TO_TXT,				// 将epub文件解压出来的HTML文件转化为TXT文件
	TXT_TO_TXT,					// 将原本TXT文件中的xxx改为第xxx章 
	TXT_TO_TXT_DELETE_SPACE,	// 将原本TXT文件中不规则的换行删除
	LRC_TO_ASS,					// 将LRC文件转化为ASS文件
	SRT_TO_ASS,					// 将SRT文件转化为ASS文件
};

class Utils {
public:
	static Utils& Instance() {
		static Utils instance;
		return instance;
	}

	void Main(UtilsType type, string path, string fileType, string targetType);

private:
	Utils(){}

	/*
	* @brief 从给定目录中，读取所有指定文件格式的文件，保存到成员变量files中
	* @param path 指定目录
	* @param fileType 指定的文件格式，如 .jpg
	*/
	void getAllFiles();

	// 重命名文件
	void renameFiles();

private:
	string path;
	string fileType;
	string targetType;
	vector<string> files;
};

