#pragma once
#include <cstdio>

// ��LRC�ļ�ת��ΪASS�ļ�
// LRC��ʽҪ��
//  1. ʱ���: [min:second.ms], ��[00:14.01]
//  2. ���һ��: �����, ��ʾ���׸�Ľ���ʱ��
class LRC_TO_ASS {
public:
    // �������
    static bool Main(const char* path = "../doc/source.lrc", const char* output = "../doc/target.ass");

private:
    // ��LRC�ļ�����ת��ΪASS�ļ�
    static void GetText(FILE* fin, FILE* fout);

    // �������е�һ��, ����������buffer��
    static void GetOneRow(FILE* fout);
};
