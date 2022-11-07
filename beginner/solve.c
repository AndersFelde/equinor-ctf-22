#include <stdio.h>
#include <string.h>

// char *pw_old = "\/[\\XZ_+YZ/\]/].+`.ZW]XWW/*+,\[Z_00102008";
char *pw = "\\/[\\XZ_+YZ/\\]/].+`.ZW]XWW/";
int checkChar(int param_2) { return (int)(char)pw[(long)param_2 + -1]; }

int main() {
    int len = strlen(pw);
    for (int i = 0; i < len; i++) {
        // printf("")
        printf("p64(0x%X) + ", 0x90 - checkChar(i));
    }
    /* char input[] = {0x34, 0x0};
    int passwordLen = strlen(input);
    int i = 0;
    for (i = 0; i < passwordLen; i++) {
        printf("INPUT: %c  ", input[i]);
        printf("INPUT: %c  ", 0x90 - (int)input[i]);
        printf("PASSWORD: %c   ", checkChar(passwordLen - i));
        printf("PASSWORD: %c   ", checkChar(passwordLen - i) + 0x90);
        printf("PASSWORD: %c\n", checkChar(passwordLen - i) - 0x90);
    } */
}
