#include <stdio.h>
#include <string.h>

int main(void)
{
    char *key = "__stack_check";
    char buffer[100];
    
    printf("Please enter key: ");
    scanf("%s", buffer);
    
    if (strcmp(buffer, key))
        printf("Nope.\n");
    else
        printf("Good job.\n");
    
    return 0;
}
