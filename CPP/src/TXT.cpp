#pragma warning(disable : 4996)
#include <cstring>
#include <algorithm>
#include <direct.h> 

#include "../include/EPUB_TO_TXT.h"
#include "../include/TXT_TO_TXT.h"
#include "../include/TXT_TO_TXT_Delete_Space.h"
using namespace std;

static const int maxn = 10000 + 10;
static char buffer[maxn];  // ������
static char txt[maxn];     // �ı�
static char header[maxn];  // ����

// �ж�source��target��ǰlen���ַ��Ƿ���ͬ
static bool comp(const char* source, const char* target, int len) {
    for (int i = 0; i < len; i++)
        if (source[i] != target[i]) return false;
    return true;
}

/*============ EPUB_TO_TXT ============*/
bool EPUB_TO_TXT::Main(const char* sourcePath, const char* output) {
    printf("\n\033[31m=================== EPUB => TXT ===================\033[0m\n");
    printf("sourcePath = \033[32m%s\033[0m, target = \033[32m%s\033[0m\n\n", sourcePath, output);

    char path[100] = "";

    FILE* fout = fopen(output, "w");

    for (int i = 1; i <= 1; i++) {
        sprintf(path, "%s/chapter%d.html", sourcePath, i);
        FILE* fin = fopen(path, "r");

        if (fin == NULL) {  // �ļ���ʧ�ܣ�·��������
            printf("\033[32m%s\033[0m�ļ���ʧ��\n", path);
            printf("��ǰ·��Ϊ\033[33m%s\033[0m\n", getcwd(buffer, maxn));
            printf("\033[31m==================================================\033[0m\n");
            return false;
        }

        GetText(fin, fout);

        fclose(fin);

        printf("Convert \033[31m%s\033[0m Complete\n", path);
    }

    fclose(fout);

    printf("��ʽת���ɹ�, ���·��Ϊ: \033[33m%s\033[0m\n", output);
    printf("\033[31m==================================================\033[0m\n");

    return true;
}

void EPUB_TO_TXT::Delete_Angle_Brackets(Type type) {
    int len = strlen(buffer);
    int begin_index = 0, end_index = len - 1;
    if (type == Type::title) {  // �Ǳ���,ɾ��<h3></h3>
        begin_index += 4;
        end_index -= 6;
    } else if (type == Type::text) {  // ������,ɾ��<p></p>
        begin_index += 3;
        end_index -= 5;
    }
    int cnt = 0;
    for (int i = begin_index; i <= end_index; i++, cnt++)
        txt[cnt] = buffer[i];
    txt[cnt] = 0;
}

void EPUB_TO_TXT::Convert_Header() {
    int chapter = 0;
    sscanf(txt, "%d%s", &chapter, buffer);
    sprintf(header, "��%d�� %s", chapter, buffer);
}

void EPUB_TO_TXT::GetText(FILE* fin, FILE* fout) {
    while (fgets(buffer, maxn, fin)) {
        // printf("buffer=%s\n", buffer);
        if (comp(buffer, "<h3>", 4)) {
            // printf("����:%s\n", buffer+4);
            Delete_Angle_Brackets(Type::title);
            Convert_Header();
            fprintf(fout, "%s\n", header);
        }
        if (comp(buffer, "<p>", 3)) {
            // printf("����:%s\n", buffer+3);
            Delete_Angle_Brackets(Type::text);
            fprintf(fout, "%s\n", txt);
        }
    }
}


/*============ TXT_TO_TXT ============*/
bool TXT_TO_TXT::Main(const char* path, const char* output) {
    printf("\n\033[31m=================== TXT => TXT ===================\033[0m\n");
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

    fclose(fout);

    printf("��ʽת���ɹ�, ���·��Ϊ: \033[33m%s\033[0m\n", output);
    printf("\033[31m==================================================\033[0m\n");

    return true;
}

int TXT_TO_TXT::GetDigit(char*& source) {
    int len = strlen(source);
    int ans = 0, i;
    // ɾ��ǰ��Ŀո�
    while (*source == ' ')
        source++;
    // ��ȡ����
    for (i = 0; i < len; i++) {
        if (source[i] == ' ') break;
        if (source[i] > '9' || source[i] < '0') break;
        ans = ans * 10 + source[i] - '0';
    }
    source += i;
    return ans;
}

void TXT_TO_TXT::GetText(FILE* fin, FILE* fout) {
    int cnt = 0;
    while (fgets(buffer, maxn, fin)) {
        char* source = buffer;
        int digit = GetDigit(source);
        if (digit) fprintf(fout, "��%d�� ", digit);
        fputs(source, fout);

        // puts(source);
        // cnt++;
        // if (cnt == 10)break;
    }
}

/*============ TXT_TO_TXT_Delete_Space ============*/
bool TXT_TO_TXT_Delete_Space::Main(const char* path, const char* output) {
    printf("\n\033[31m=================== Delete Space ===================\033[0m\n");
    printf("source = \033[32m%s\033[0m, target = \033[32m%s\033[0m\n\n", path, output);

    FILE* fin = fopen(path, "r");
    FILE* fout = fopen(output, "w");

    if (fin == NULL) {  // �ļ���ʧ�ܣ�·��������
        printf("\033[32m%s\033[0m�ļ���ʧ��\n", path);
        printf("��ǰ·��Ϊ\033[33m%s\033[0m\n", getcwd(buffer, maxn));
        printf("\033[31m==================================================\033[0m\n");
        return false;
    }

    char buffer[maxn];
    while (fgets(buffer, maxn, fin)) {
        int len = strlen(buffer);
        if (len <= 1) continue;

        buffer[len - 1] = 0;

        if (buffer[0] == -29) fprintf(fout, "\n");

        fprintf(fout, "%s", buffer);
        // fprintf(fout, "No.%d:'%d' %s", i, (int)buffer[0], buffer);
    }

    fclose(fout);

    printf("��ʽת���ɹ�, ���·��Ϊ: \033[33m%s\033[0m\n", output);
    printf("\033[31m==================================================\033[0m\n");

    return true;
}

