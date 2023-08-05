Monoalpha by Toby Govin-Fowler

Version 1.0.0

Monoalpha is a simple monoalphabetic cipher program. It can be used to generate generate code
alphabets, as well as encrypting, and decrypting text. It supports caesar shift,
ROT13, affine, atbash, and keyword ciphers. It can also encrypt and decrypt based
on your own code alphabets.

Commands (words in [square brackets] indicate arguments)

alphatrans

Encrypts/decrypts based on [alphabet one] and [alphabet two].

encrypt

Encrypts [plaintext] using a [code alphabet].

decrypt

Decrypts [plaintext] using a [code alphabet].

caesar

Gives caesar shift code alphabet based on [offset].

rot13

Gives code alphabet for ROT13 cipher.

affine

Gives code alphabet for affine cipher based on values [a] and [b].

atbash

Gives code alphabet for atbash cipher.

keyword

Gives keyword code alphabet based on [keyword].

caesar_encrypt

Applies caesar shift to [plaintext] using [offset].

caesar_decrypt

Reverses caeser shift on [coded text] using [offset].

rot13_encrypt

Applies ROT13 cipher to [plaintext].

rot13_decrypt

Decrypts ROT13 cipher on [coded text].

affine_encrypt

Applies affine cipher to [plaintext] using values [a] and [b].

affine_decrypt

Reverses affine cipher on [plaintext] using values [a] and [b].

atbash_encrypt

Applies atbash cipher to [plaintext].

atbash_decrypt

Reverses atbash cipher on [plaintext].

keyword_decrypt

Applies keyword cipher to [plaintext] using [keyword].

keyword_decrypt

Reverses keyword cipher on [plaintext] using [keyword].