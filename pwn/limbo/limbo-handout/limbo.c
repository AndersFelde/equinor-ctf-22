#define _GNU_SOURCE
#include <link.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <signal.h>
#include <unistd.h>
#include <stdbool.h>
#define NUM_BYTES 2
#define LIBC_TEXT_SIZE 0x195000


void * libc_address;
void ignore_me_init_buffering() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void kill_on_timeout(int sig) {
    if (sig == SIGALRM) {
        printf("[!] Anti DoS Signal. Patch me out for testing.");
        _exit(0);
    }
}

void ignore_me_init_signal() {
    signal(SIGALRM, kill_on_timeout);
    alarm(60);
}

int endswith(const char *str, const char *suffix) {
    if (!str || !suffix)
        return 0;
    size_t lenstr = strlen(str);
    size_t lensuffix = strlen(suffix);
    if (lensuffix >  lenstr)
        return 0;
    return strncmp(str + lenstr - lensuffix, suffix, lensuffix) == 0;
}


static int callback(struct dl_phdr_info *info, size_t size, void *data) {
    char *type;
    int p_type, j;
    if (endswith(info->dlpi_name, "libc.so.6")) {
        for (j = 0; j < info->dlpi_phnum; j++) {
            if (info->dlpi_phdr[j].p_flags == 0x5) {
                if ( mprotect( (void *) (info->dlpi_addr + info->dlpi_phdr[j].p_vaddr), LIBC_TEXT_SIZE, PROT_READ|PROT_EXEC|PROT_WRITE) < 0 ) {
                    printf("mprotect() error");
                    return 1337;
                }
                libc_address = (void *) (info->dlpi_addr + info->dlpi_phdr[j].p_vaddr);
                
            }
        }
    }
    return 0;
}

void banner() {
    FILE *fptr;
    fptr = fopen("limbo.ans", "r");
    if (fptr == NULL)
    {
        printf("Cannot open file \n");
        exit(0);
    }
    char c;
    c = fgetc(fptr);
    while (c != EOF)
    {
        printf ("%c", c);
        c = fgetc(fptr);
    }
  
    fclose(fptr);
}

int main(int argc, char *argv[]) {
    ignore_me_init_buffering();
    ignore_me_init_signal();
    banner();
    // make libc RWX
    dl_iterate_phdr(callback, NULL);



    char buffer[20];
    printf ("libc .text @ [%p-%p]\n", libc_address, libc_address+LIBC_TEXT_SIZE);
    printf("write to\n> ");
    fgets(buffer, 20, stdin);
    long address = (long)strtol(buffer, NULL, 0);
    memset(buffer, '\x00', 20);
    if (address < (long)libc_address || address > (long)libc_address+LIBC_TEXT_SIZE-NUM_BYTES) {
        puts("Error! that address it outside the libc .text area!");
        return 1337;
    }
    printf ("What to write? [Maximum number of bytes: %d] \n> ", NUM_BYTES);
    
    fgets(buffer, 20, stdin);
    memcpy((void*)address, buffer, NUM_BYTES);
    memset(buffer, '\x00', 20);
    printf("wrote %.2s to %p\n", buffer, (void*)address);
    
    exit(1);
}