# uas_pimo_topic_modeling_philoit
Project Final Topic Modeling PhiloIT

Anggota Kelompok
Edward – 1872002
Michael Sebastian – 1872005
Juan David - 1872008
Rolando Vieri – 1872010
Anthony Halim - 1872027

Langkah-langkah instalasi:
1.) Install library yang diperlukan dengan menuliskan “pip install <namalibrary>” pada terminal. Untuk library yang diperlukan diantaranya adalah:
flask, numpy, pandas, re, gensim, spacy, pyLDAvis, matplotlib, Sastrawi, nltk, dan wordcloud.
2.) Untuk menjalankan localhost website, buka terminal pada direktori yang sama dengan app.py, kemudian jalankan perintah “python -W ignore app.py”
3.) Masukkan alamat “localhost:5000” pada browser

Langkah-langkah penggunaan mencari topik modeling:
1.) Memasukkan tanggal awal dan tanggal akhir sesuai format tanggal yang tertera.
2.) Menekan tombol “Find Topic”
3.) Tunggu proses pemodelan topik hingga selesai hingga hasil topik muncul pada tabel.

Langkah-langkah melihat detail topik:
1.) Menekan hyperlink pada tabel pada kolom nomor
2.) Halaman detail akan terbuka yang berisi wordcloud dari kata kunci yang terdapat pada topik tersebut.

Langkah-langkah melakukan download CSV:
1.) Memasukkan tanggal awal dan tanggal akhir sesuai format tanggal yang tertera.
2.) Menekan tombol “Download CSV”.
3.) File CSV akan tersimpan pada komputer.
