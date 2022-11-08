#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

// gcc -static -z execstack -z norelro -fno-stack-protector -o format1 format1.c
// Ref. https://exploit-exercises.com/protostar/format1/

int target;

void vuln(char *str)
{

    printf(str);

    if (target)
    {
        printf("you have modified the target :)\n");
        printf("value of target: %d\n", target);
    }
}

int main(void)
{
    char string[256];
    printf("input your string motherfucker\n");
    fgets(string, 256, stdin);
    vuln(string);
}