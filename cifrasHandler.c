#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main () {

    FILE * fp;
    FILE * fp2;
    FILE * fp3;
    char current_char, to_replace = 'Z';
    int i, j, test = 1;
    fp3 = fopen("execution.bat", "w");

    for(i = 0; i < 16000; i = i+10){

        fp = fopen("cifras.js", "r");

        j = i + 10;
        printf("\n%d %d", i, j);

        char name[100];
        strcpy(name,"cifra_");
        char number[6];
        char number2[6];
        sprintf(number, "%d", i);
        sprintf(number2, "%d", j);
        printf("\n%s", number);
        strcat(name, number);
        strcat(name,".js");

        printf("\n%s", name);

        fp2 = fopen(name, "w");
        fputs("node ", fp3);
        fputs(name, fp3);
        fputc('\n', fp3);

        test = 1;

        while (((current_char  = fgetc(fp)) != EOF) && (test == 1)) {     
            if (current_char == to_replace) {

                fseek(fp, ftell(fp) - 1, SEEK_SET);
                
                int k;
                for(k = 0; k < 5; k++){
                    if(number[k]>'9' || number[k]<'0'){
                        number[k] = ' ';
                    }
                }

                fprintf(fp2, "%c", number[0]);
                fprintf(fp2, "%c", number[1]);
                fprintf(fp2, "%c", number[2]);
                fprintf(fp2, "%c", number[3]); 
                fprintf(fp2, "%c", number[4]);
                fgetc(fp);
                printf("\nhey");
                test = 0;

            }
            else {
                fprintf(fp2, "%c", current_char);
            }                              
        }

        while ((current_char  = fgetc(fp)) != EOF) {     
            if (current_char == to_replace) {

                fseek(fp, ftell(fp) - 1, SEEK_SET);
                
                int k;
                for(k = 0; k < 5; k++){
                    if(number2[k]>'9' || number2[k]<'0')
                        number2[k] = ' ';
                }

                fprintf(fp2, "%c", number2[0]);
                fprintf(fp2, "%c", number2[1]);
                fprintf(fp2, "%c", number2[2]);
                fprintf(fp2, "%c", number2[3]); 
                fprintf(fp2, "%c", number2[4]);
                fgetc(fp);

            }
            else {
                fprintf(fp2, "%c", current_char);
            }                              
        }
        
        fclose(fp2);
        fclose(fp);
    }
    fclose(fp3);
    return 0;
}