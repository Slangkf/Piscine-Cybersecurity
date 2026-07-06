#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

void nope(void)
{
    puts("Nope.");
    exit(1);
    
}

int good_job(void)
{
    return puts("Good job.");
}

int main(void)
{
    printf("Please enter key: ");
    char input[24];
    
    if (1 != scanf("%23s", input))
    {
        nope();
    }
    
    if ('2' != input[1])
    {
        nope();
    }
    
    if ('4' != input[0])
    {
        nope();  
    }
    
    fflush(stdin);
    
    char key[9];
    memset(&key, 0, 9);
    key[0] = '*';
    
    size_t i = 2;
    size_t j = 1;
    
    while (true)
    {
        int flag = 0;
        if (strlen(key) < 8)
        {
            flag = i < strlen(input);
        }

        if (flag == 0)
            break;

        char buffer[4];
        memset(&buffer, 0, 4);
        strncpy(buffer, &input[i], 3);
        key[j] = atoi(buffer);
        i += 3;
        j += 1;
    }
    
    key[j] = 0;
    
    switch (strcmp(key, "********"))
    {
        case 0:
        {
            good_job();
            return 0;
        }
        case 1:
        {
            nope();
            return 1;
        }
        case 2:
        {
            nope();
            return 1;
        }
        case 3:
        {
            nope();
            return 1;
        }
        case 4:
        {
            nope();
            return 1;
        }
        case 5:
        {
            nope();
            return 1;
        }
        case 115:
        {
            nope();
            return 1;
        }
        case 4294967294:
        {
            nope();
            return 1;
        }
        case 4294967295:
        {
            nope();
            return 1;
        }
    }
    nope();
    return 1;
}
