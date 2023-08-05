/*
version 20080913
D. J. Bernstein
Public domain.
*/

#include "crypto_core_hsalsa20.h"
#include "crypto_stream_salsa20.h"
#include "crypto_stream_xsalsa20.h"
#include "utils.h"

int crypto_stream_xsalsa20_xor_ic(
        unsigned char *c,
  const unsigned char *m,unsigned long long mlen,
  const unsigned char *n,uint64_t ic,
  const unsigned char *k
)
{
  unsigned char subkey[32];
  int ret;
  crypto_core_hsalsa20(subkey,n,k,NULL);
  ret = crypto_stream_salsa20_xor_ic(c,m,mlen,n + 16,ic,subkey);
  sodium_memzero(subkey, sizeof subkey);
  return ret;
}

int crypto_stream_xsalsa20_xor(
        unsigned char *c,
  const unsigned char *m,unsigned long long mlen,
  const unsigned char *n,
  const unsigned char *k
)
{
  return crypto_stream_xsalsa20_xor_ic(c, m, mlen, n, 0ULL, k);
}
