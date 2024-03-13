#pragma once
#include <cstdio>

// 将原本TXT文件中不规则的换行删除
class TXT_TO_TXT_Delete_Space {
public:
    static bool Main(const char* path = "../doc/source.txt", const char* output = "../doc/target.txt");
};
