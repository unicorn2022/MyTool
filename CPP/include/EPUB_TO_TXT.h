#pragma once
#include <cstdio>

// ��epub�ļ���ѹ������HTML�ļ�����ת��ΪTXT�ļ�
class EPUB_TO_TXT {
public:
    static bool Main(const char* sourcePath = "../doc", const char* output = "../doc/target.txt");

private:
    enum Type {
        title,
        text
    };

    // ��<h3></h3>��<p></p>ɾ��
    // buffer==>txt
    static void Delete_Angle_Brackets(Type type);

    // ������ĳɵ�xxx��
    // txt==>header
    static void Convert_Header();


    // ��HTML�е�������ȡ����
    static void GetText(FILE* fin, FILE* fout);
};