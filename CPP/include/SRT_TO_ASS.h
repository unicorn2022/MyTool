#pragma once
#include <cstdio>

// ��SRT�ļ�ת��ΪASS�ļ�
class SRT_TO_ASS {
public:
    // �������
    static bool Main(const char* path = "../doc/source.srt", const char* output = "../doc/target.ass");

private:
    // ��LRC�ļ�����ת��ΪASS�ļ�
    static void GetText(FILE* fin, FILE* fout);

    // �������е�һ��, ����������buffer��
    static void GetOneRow(FILE* fout);
};
