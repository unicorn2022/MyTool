#pragma warning(disable : 4996)
#include <cstring>
#include <algorithm>
#include <direct.h>
#include <string>
#include <vector>

#include "../include/SRT_TO_ASS.h"
using namespace std;

static const int maxn = 100000 + 10;
static char buffer[maxn];   // ������
const bool ChineseFirst = false;    // ������Ļ: �Ƿ���������

bool SRT_TO_ASS::Main(const char* path, const char* output) {
    printf("\n\033[31m=================== SRT => ASS ===================\033[0m\n");
    printf("source = \033[32m%s\033[0m, target = \033[32m%s\033[0m\n\n", path, output);


    FILE* fin = fopen(path, "r");
    FILE* fout = fopen(output, "w");

    if (fin == NULL) {  // �ļ���ʧ�ܣ�·��������
        printf("\033[32m%s\033[0m�ļ���ʧ��\n", path);
        printf("��ǰ·��Ϊ\033[33m%s\033[0m\n", getcwd(buffer, maxn));
        printf("\033[31m==================================================\033[0m\n");
        return false;
    }

    GetText(fin, fout);

    fclose(fin);
    fclose(fout);

    printf("��ʽת���ɹ�, ���·��Ϊ: \033[33m%s\033[0m\n", output);
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

void SRT_TO_ASS::GetText(FILE* fin, FILE* fout) {

    // �������ͷ
    for (auto s : header) {
        fprintf(fout, "%s", s.c_str());
    }

    // ��LRC�е�ÿһ��, ��Ӧ��ASS�е�һ��
    while (fgets(buffer, maxn, fin)) {
        GetOneRow(fout);
    }
}

void SRT_TO_ASS::GetOneRow(FILE* fout) {
    static string startTime = "";
    static string endTime = "";
    static string lastStartTime = "";
    static bool isTimeLine = true;

    string line(buffer);

    // ��ȡ��ǰ��ʵĿ�ʼʱ��
    if (isTimeLine) {
        if (line.size() < 12) return;
        lastStartTime = startTime;
        startTime = line.substr(0, 8) + "." + line.substr(9, 2);
        endTime = line.substr(17, 8) + "." + line.substr(26, 2);
        isTimeLine = false;
        return;
    }

    // ��ȡ��ǰ�������
    if (line.empty()) return;

    isTimeLine = true;
    // �����ʶ�Ӧ��ASS����
    fprintf(fout, "Dialogue: 0,%s,%s,", startTime.c_str(), endTime.c_str()); // ʱ��
    // �ڶ��и��
    if (startTime == lastStartTime) {
        if(ChineseFirst)fprintf(fout, "Japanese,NTP,0000,0000,0000,,");  // ���actor�����롢��Ч
        else  fprintf(fout, "Chinese,NTP,0000,0000,0000,,");  // ���actor�����롢��
    }
    else {
        if (ChineseFirst)fprintf(fout, "Chinese,NTP,0000,0000,0000,,");  // ���actor�����롢��Ч
        else  fprintf(fout, "Japanese,NTP,0000,0000,0000,,");  // ���actor�����롢��
    }
    fprintf(fout, "%s", line.c_str());         // ���
}