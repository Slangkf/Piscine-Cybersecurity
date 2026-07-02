#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int ok()
{
    return puts("Good job.");
}

void no()
{
    puts("Nope.");
    exit(1);
}

int main(void)
{
    printf("Please enter key: ");
    char buf[24];
    
    if (1 != scanf("%23s", buf))
    {
        no();
    }
    
    if ('0' != buf[0])
    {
        no();
    }

    if ('0' != buf[1])
    {
        no();
    }
    
    fflush(stdin);
   
    char key[9];
    memset(&key, 0, 9);
    key[0] = 'd';
   
    size_t i = 2;
    size_t j = 1;
    
    while (true)
    {
        int flag = 0;
        if (strlen(key) < 8)
        {
            flag = i < strlen(buf);
        }

        if (flag == 0)
            break;
        
        char letter[4];
        memset(&letter, 0, 4);
        strncpy(letter, &buf[i], 3);
        key[j] = atoi(letter);
        i += 3;
        j += 1;
    }
    
    key[j] = 0;
    
    if (strcmp(key, "delabere"))
    {
        no();
    }
    
    ok();
    return 0;
}
