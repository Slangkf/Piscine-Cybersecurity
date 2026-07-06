#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int ok(void)
{
    return puts("Good job.");
}

void no(void)
{
    puts("Nope.");
    exit(1);
}

int main(void)
{
    printf("Please enter key: ");
    char input[24];
    
    if (1 != scanf("%23s", input))
    {
        no();
    }
    
    if ('0' != input[1])
    {
        no();
    }

    if ('0' != input[0])
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
    
    if (strcmp(key, "delabere"))
    {
        no();
    }
    
    ok();
    return 0;
}
