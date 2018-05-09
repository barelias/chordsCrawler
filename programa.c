#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {

    int i, nalunos;
    scanf ("%d", &nalunos);
    double notas[nalunos], total = 0;
    int index[nalunos];
    char alunos[nalunos][100];
    for (i = 0; i < nalunos; i++) {
        notas[i] = 0;
        scanf ("%s", &alunos[i]);
        getc(stdin);  
        scanf ("%d", &notas[i]);
        getc(stdin);
        total += notas[i];
    }
    double media = total/nalunos;
    for (i = 0; i < nalunos; i++) {
        if (notas[i] > media) {
            fputs(strcat(alunos[i], "\n"), stdout);
        }
    }
    return 0;
}