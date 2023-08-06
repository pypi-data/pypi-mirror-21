#include <stdlib.h>
#include <stdio.h>
#include "pool.h"

void print_pool(Pool *pool) {
    int i;
    for (i=0; i!=pool->count; i++) {
        printf("%d ", *(int*) pool->members[i]);
    }
    printf("\n");
}

int main() {
    Pool *pool = pool_new(sizeof(int*), 4);

    int a, b, c;
    a = 16;
    b = 1;
    c = 2;
    pool_add(pool, (char*) &a);
    pool_add(pool, (char*) &b);
    pool_add(pool, (char*) &c);

    print_pool(pool);
    pool_pop(pool, 2);
    print_pool(pool);

    return 0;
}

