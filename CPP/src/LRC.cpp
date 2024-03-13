#pragma warning(disable : 4996)
#include <cstring>
#include <algorithm>
#include <direct.h>
#include <string>
#include <vector>

#include "../include/LRC_TO_ASS.h"
using namespace std;

static const int maxn = 100000 + 10;
static char buffer[maxn];   // 缓存区

bool LRC_TO_ASS::Main(const char* path, const char* output) {
    printf("\n\033[31m=================== LRC => ASS ===================\033[0m\n");
    printf("source = \033[32m%s\033[0m, target = \033[32m%s\033[0m\n\n", path, output);


    FILE* fin = fopen(path, "r");
    FILE* fout = fopen(output, "w");

    if (fin == NULL) {  // 文件打开失败，路径不存在
        printf("\033[32m%s\033[0m文件打开失败\n", path);
        printf("当前路径为\033[33m%s\033[0m\n", getcwd(buffer, maxn));
        printf("\033[31m==================================================\033[0m\n");
        return false;
    }

    GetText(fin, fout);

    fclose(fin);
    fclose(fout);

    printf("格式转换成功, 输出路径为: \033[33m%s\033[0m\n", output);
    printf("\033[31m==================================================\033[0m\n");

    return true;
}

static const vector<string> header = {
    "[V4+ Styles]\n",  //
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
    "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n",                 //
    "Style: Japanese,Arial,10,&H00FFFFFF,&H00FFB100,&H00FF00FF,&H00000000,0,0,0,0,100.00,100.00,0.00,0.00,1,1.00,0.00,2,10,10,0,1\n",  //
    "Style: Chinese,Arial,16,&H00058DF8,&H00C080FF,&H00FFFFFF,&HFFFFFFFF,0,0,0,0,100.00,100.00,2.00,0.00,2,1.00,1.00,2,0,0,0,134\n",  //
    "\n",                                                                                                                             //
    "[Events]\n",                                                                                                                     //
    "Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n"                                              //
};

void LRC_TO_ASS::GetText(FILE* fin, FILE* fout) {

    // 先输出标头
    for (auto s : header) {
        fprintf(fout, "%s", s.c_str());
    }

    // 对LRC中的每一行, 对应于ASS中的一行
    while (fgets(buffer, maxn, fin)) {
        GetOneRow(fout);
    }
}

void LRC_TO_ASS::GetOneRow(FILE* fout) {
    static string lastTime = "";
    static string lastLRC = "";
    static string nowTime = "";
    static string nowLRC = "";

    string line(buffer);

    // 读取当前歌词的开始时间
    size_t pos = line.find(']');
    lastTime = nowTime;
    nowTime = line.substr(1, pos - 1);

    // 读取当前歌词内容
    lastLRC = nowLRC;
    nowLRC = line.substr(pos + 1);

    if (lastLRC.empty()) return;

    // 输出上一句歌词对应的ASS内容
    fprintf(fout, "Dialogue: 0,0:%s,0:%s,", lastTime.c_str(), nowTime.c_str()); // 时间
    fprintf(fout, "Chinese,NTP,0000,0000,0000,,");  // 风格、actor、对齐、特效
    fprintf(fout, "%s", lastLRC.c_str());         // 歌词
}