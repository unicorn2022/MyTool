#pragma warning(disable : 4996)

#include "../include/Utils.h"
#include "../include/main.h"

bool Work(string command, string fileType, string targetType);

int main() {
    bool firstline = true;

    while (true) {
        if (!firstline) printf("\n");
        else firstline = false;

        /* 输入信息 */
        CommandHelp();
        // 选择功能
        string command;
        SetConsoleColor(ConsoleColor::Yellow);
        printf("请输入本次要使用的功能, 或者退出程序:");
        SetConsoleColor(ConsoleColor::Red);
        cin >> command;
        if (command.compare("exit") == 0) break;

        string fileType, targetType;
        if (command.compare("rename") == 0) {
            // 源文件类型
            SetConsoleColor(ConsoleColor::Yellow);
            printf("请输入源文件类型:");
            SetConsoleColor(ConsoleColor::Red);
            cin >> fileType;
            if (fileType.compare("exit") == 0) continue;
            

            // 目标文件类型
            SetConsoleColor(ConsoleColor::Yellow);
            printf("请输入目标文件类型:");
            SetConsoleColor(ConsoleColor::Red);
            cin >> targetType;
            if (targetType.compare("exit") == 0) continue;
            
        }

        /* 进行批处理 */
        while (Work(command, fileType, targetType));
    }

    SetConsoleColor(ConsoleColor::Clear);
    return 0;
}

bool Work(string command, string fileType, string targetType) {

    UtilsType type = UtilsType::NONE;
    for (int i = 0; i < UtilsTypeString.size(); i++) {
        size_t id = UtilsTypeString[i].find_first_of(" ");
        string now = UtilsTypeString[i].substr(0, id);
        if (command.compare(now) == 0)
            type = static_cast<UtilsType>(i);
    }

    /* 根据指令类型, 设置文件类型 */
    switch (type) {
    case UtilsType::EPUB_TO_TXT:
        fileType = "html";
        targetType = "txt";
        break;
    case UtilsType::TXT_TO_TXT:
        fileType = "txt";
        targetType = "txt";
        break;
    case UtilsType::TXT_TO_TXT_DELETE_SPACE:
        fileType = "txt";
        targetType = "txt";
        break;
    case UtilsType::LRC_TO_ASS:
        fileType = "lrc";
        targetType = "ass";
        break;
    case UtilsType::SRT_TO_ASS:
        fileType = "srt";
        targetType = "ass";
        break;
    case UtilsType::NONE:
        SetConsoleColor(ConsoleColor::White);
        printf("非法指令\n");
        return false;
    }

    string path;
    SetConsoleColor(ConsoleColor::Yellow);
    printf("请输入源文件路径:");
    SetConsoleColor(ConsoleColor::Red);
    cin >> path;
    SetConsoleColor(ConsoleColor::Clear);

    if (path.compare("exit") == 0) return false;    

    Utils::Instance().Main(type, path, fileType, targetType);

    return true;
}