#include "vcashhash.h"
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>

#include "sha3/sph_blake.h"
#include "sha3/sph_whirlpool.h"


void blake_hash(const char* input, char* output)
{
    sph_blake256_context ctx_blake;

    sph_blake256_init(&ctx_blake);

    sph_blake256 (&ctx_blake, input, 80);

    sph_blake256_close (&ctx_blake, output);
}


void whirlpoolx_hash(const char* input, char* output)
{
    unsigned char hash[64];

    memset(hash, 0, sizeof(hash));

    sph_whirlpool_context ctx_whirlpool;

    sph_whirlpool_init(&ctx_whirlpool);

    sph_whirlpool(&ctx_whirlpool, input, 80);

    sph_whirlpool_close(&ctx_whirlpool, hash);

    unsigned char hash_xored[sizeof(hash) / 2];
    unsigned int i = 0;

    for (; i < (sizeof(hash) / 2); i++)
    {
        hash_xored[i] =
            hash[i] ^ hash[i + ((sizeof(hash) / 2) / 2)]
        ;
    }

    memcpy(output, hash_xored, 32);
}
