#pragma once
#include <cstdio>

// ��ԭ��TXT�ļ��е�xxx��Ϊ��xxx��
// ע��,ֻ���ڱ����г��ֿո�
class TXT_TO_TXT {
public:
    // �������
    static bool Main(const char* path = "../doc/source.txt", const char* output = "../doc/target.txt");

private:
    // ���������,�򷵻����ֵ�ֵ,����sourceָ�����
    // ���򷵻�0
    static int GetDigit(char*& source);


    // �Իس��ָ�ı�����ȫ����ȡ����
    // ���������,����ӵ�xxx��
    static void GetText(FILE* fin, FILE* fout);
    
};
