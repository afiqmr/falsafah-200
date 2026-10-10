"""Build notes.json (the Nota tab) from the exam-note documents in notes_source/.

Each topic combines:
  - a condensed summary (key question, numbered cards, steps, formula), transcribed
    from the "Nota Ringkas Exam" infographics, and
  - the full explanation paragraphs from the matching Word document. Each card is
    linked to its document section by section number.

Usage:  python build_notes.py   (then run build.py)
"""
import html
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / 'notes_source'


def read_docx(name):
    """Return {'intro': section, 'sections': {num: section}, 'closing': [sections]}."""
    xml = zipfile.ZipFile(SRC / name).read('word/document.xml').decode('utf-8')
    paras = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', xml, re.S):
        style = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        text = html.unescape(''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', p, re.S))).strip()
        if text:
            paras.append((style.group(1) if style else '', text))

    sections, cur = [], None
    for style, text in paras:
        if style == 'Title' or text.startswith('Disediakan oleh'):
            continue
        if style.startswith('Heading'):
            m = re.match(r'^(\d+)\s+(.*)$', text)
            cur = {'num': int(m.group(1)) if m else None, 'heading': m.group(2) if m else text, 'paras': [], 'refs': []}
            sections.append(cur)
        elif cur is not None:
            (cur['refs'] if text.startswith('Rujukan') else cur['paras']).append(text)

    numbered = {s['num']: s for s in sections if s['num'] is not None}
    intro = sections[0] if sections and sections[0]['num'] is None else None
    closing = [s for s in sections[1:] if s['num'] is None]
    return {'intro': intro, 'sections': numbered, 'closing': closing}


def details(sec):
    return {'paras': sec['paras'], 'refs': sec['refs']}


def item(no, name, tag, desc, contoh=None, sec=None, flow=None):
    d = {'no': no, 'name': name, 'tag': tag, 'desc': desc}
    if contoh:
        d['contoh'] = contoh
    if flow:
        d['flow'] = flow
    if sec is not None:
        d['details'] = details(sec)
    return d


def general_sections(doc, nums):
    out = []
    for n in nums:
        s = doc['sections'][n]
        out.append({'heading': s['heading'], 'paras': s['paras'], 'refs': s['refs']})
    for s in doc['closing']:
        out.append({'heading': s['heading'], 'paras': s['paras'], 'refs': s['refs']})
    return out


def lead(doc):
    i = doc['intro']
    return {'tagline': i['heading'], 'paras': i['paras'], 'refs': i['refs']}


# ---------------------------------------------------------------- Khitab Hilalul Wasil
k = read_docx('Nota Exam Khitab Hilalul Wasil.docx')
S = k['sections']
khitab = {
    'id': 'khitab',
    'short': 'Khitab Hilalul Wasil',
    'title': 'Khitab Hilalul Wasil',
    'istilah': 'Istilah karya: Khitab Hilaalul Washil',
    'basis': 'Berdasarkan kerangka Al Fathun Nawa · Jilid 9',
    'lead': lead(k),
    'key': {
        'q': 'Apakah ayat atau kalimah lain yang membantu menerangkan pengertian ini?',
        'pills': ['Ayat menerangkan ayat', 'Kalimah diperjelaskan melalui ayat'],
        'text': 'Bacuhan pentafshilan: mengadunkan huraian dengan menunjukkan hubungan makna yang berasas.',
    },
    'groups': [{
        'heading': '8 Subkaedah',
        'items': [
            item(1, 'Kaukaba Bil Munir', 'Lafaz berkaitan', 'Hubungkan kalimah yang sama atau berkaitan antara ayat.', 'Ali Imran 3:191 ↔ Ar Rum 30:8', S[3]),
            item(2, 'Thamarun Bil Munir', 'Sifat dan definisi', 'Kenal pasti sekurang-kurangnya 3 sifat hakiki dan ayat pendefinisi.', 'Ali Imran 3:200 ↔ Al Baqarah 2:45', S[4]),
            item(3, 'Tafshiilul ‘Aqid', 'Huraian dalam ayat', 'Kenal pasti mulk, maudha’ dan khitab; teliti keterangan berturutan.', 'Hud 11:15', S[5]),
            item(4, 'Bayaanul Ma’ani', 'Perlakuan dan akibat', 'Gunakan ayat penerang untuk menghuraikan kesan sesuatu perlakuan.', 'Az Zukhruf 43:36 ↔ Al Baqarah 2:268', S[6]),
            item(5, 'Faqqihil Muraad', 'Bezakan istilah', 'Teliti lafaz berlainan yang kelihatan serupa dalam terjemahan.', 'Al Baqarah 2:156 ↔ Ali Imran 3:158', S[7]),
            item(6, 'Tafshiilul Jalil', 'Rantai huraian', 'Ikuti hubungan khitab hingga mesej keseluruhan ayat.', 'Al Baqarah 2:26', S[8]),
            item(7, 'Ruhul Idhafa’', 'Pihak dan taraf', 'Teliti sandaran kenyataan kepada Tuhan dan manusia menurut kerangka pengarang.', 'Al Fatihah 1:5 ↔ Muhammad 47:7', S[9]),
            item(8, 'Hilalul Khusuf', 'Kekaburan diperjelaskan', 'Dalami kalimah yang pengertiannya masih terlindung.', 'At Taubah 9:103', S[10]),
        ],
    }],
    'steps': {'heading': '5 Langkah Latihan', 'items': ['Pilih kalimah', 'Cari penerang', 'Semak konteks', 'Jelaskan hubungan', 'Rumuskan makna']},
    'example': {
        'heading': 'Contoh · Kaukaba Bil Munir',
        'title': 'Ali Imran 3:191 ↔ Ar Rum 30:8',
        'lines': [
            'Lafaz berkaitan: berfikir.',
            'Teliti perkara yang difikirkan dan konteks penciptaan dalam kedua-dua ayat.',
            'Persamaan lafaz ialah titik mula; kaitan makna perlu dijelaskan.',
        ],
    },
    'formula': {'heading': 'Formula Ingatan', 'chips': ['Lafaz', 'Definisi', 'Dalam ayat', 'Akibat', 'Beza istilah', 'Rantai', 'Taraf', 'Kekaburan']},
    'notes': {
        'heading': 'Nota Ketepatan',
        'items': [
            'Tafshiilul ‘Aqid dan Tafshiilul Jalil mempunyai pertindihan.',
            'Pendahuluan menyebut 7; huraian lengkap turut menambah Hilalul Khusuf sebagai kaedah ke-8.',
            'Istilah dan contoh mengikuti penggunaan pengarang.',
        ],
    },
    'sections': general_sections(k, [1, 2, 11, 12, 13]),
    'ref': 'Jilid 9, ms. 175–231 dan 242–244',
}

# ---------------------------------------------------------------- Syariah Khofiah
s = read_docx('Nota Exam Syariah Khofiah.docx')
S = s['sections']
syariah = {
    'id': 'syariah',
    'short': 'Syariah Khofiah',
    'title': 'Syariah Khofiah',
    'istilah': 'Istilah karya: Syariat Khafiah',
    'basis': 'Berdasarkan kerangka Al Fathun Nawa · Jilid 6 dan 9',
    'lead': lead(s),
    'key': {
        'q': 'Apakah yang ayat ini mendidik saya untuk fahami dan lakukan?',
        'text': 'Mengklasifikasikan arah didikan ayat dan menerapkannya sebagai pegangan serta amalan kehidupan.',
    },
    'groups': [{
        'heading': '10 Cabang Utama',
        'items': [
            item(1, 'Rabbi Amri', 'Pekerjaan Tuhan', 'Perhatikan penciptaan dan pengaturan alam.', 'Ibrahim 14:19', S[3]),
            item(2, 'Khitaabul ‘Ajil', 'Perintah disegerakan', 'Fahami perintah dan sambut petunjuk dengan sungguh-sungguh.', 'Ali Imran 3:200', S[4]),
            item(3, 'Baalighatul Aayah', 'Ayat kematangan', 'Bentuk disiplin dan kesediaan memikul tanggungjawab.', 'Al Muddaththir 74:1–7', S[5]),
            item(4, 'Nidaa ul Kubraa', 'Doa agung', 'Fahami permohonan dan hubungkan doa dengan usaha.', 'An Naml 27:19', S[6]),
            item(5, 'Fathul ‘Arif', 'Pembukaan pengenalan', 'Kenali Tuhan melalui kenyataan wahyu.', 'Taha 20:14', S[7]),
            item(6, 'Rafi’ul Hayat', 'Ketinggian hidup', 'Tingkatkan mutu kehidupan melalui ilmu, usaha dan amal.', 'An Najm 53:39–40', S[8]),
            item(7, 'Amthaalul Hilal', 'Penzahir sumber', 'Kaji sumber dan zahirkan manfaatnya secara bertanggungjawab.', 'Al Hadid 57:25', S[9]),
            item(8, 'Nurul ‘Ibrah', 'Cahaya pengajaran', 'Ambil teladan dan sempadan daripada kisah.', 'Yusuf 12:111', S[10]),
            item(9, 'Hujjatul Ihsaan', 'Hujah terbaik', 'Susun bukti dan sampaikan penerangan dengan baik.', 'An Nahl 16:125', S[11]),
            item(10, 'Bayaanul ‘Aqid', 'Kenyataan pokok pegangan', 'Fahami prinsip dan selaraskan tindakan dengan petunjuk.', 'Ar Rum 30:30', S[12]),
        ],
    }],
    'steps': {
        'heading': '5 Langkah Membaca',
        'items': ['Ayat', 'Kaedah tafsir', 'Peringatan', 'Kenyataan', 'Resolusi'],
        'note': 'Resolusi: rumusan arah tindakan selepas memahami ayat.',
    },
    'lists': [{'heading': 'Format Jawapan Exam', 'items': ['Nama dan definisi', 'Dalil ayat', 'Alasan pengelasan', 'Kepentingan', 'Rupa amalan', 'Rumusan']}],
    'example': {
        'heading': 'Contoh Aplikasi · Nidaa ul Kubraa',
        'lines': [
            'An Naml 27:19: Syukur → Amal salih → Rahmat Tuhan.',
            'Rupa amalan: fahami nikmat dan gunakannya untuk kebaikan.',
        ],
    },
    'formula': {'heading': 'Formula Ingatan', 'chips': ['Pekerjaan', 'Perintah', 'Kematangan', 'Doa', 'Pengenalan', 'Peningkatan', 'Sumber', 'Pengajaran', 'Hujah', 'Pegangan']},
    'notes': {
        'heading': 'Nota',
        'items': [
            'Huraian dan contoh mengikuti kerangka pengarang.',
            'Semak konteks ayat serta kaitan antara petunjuk dan amalan.',
        ],
    },
    'sections': general_sections(s, [1, 2, 13, 14, 15]),
    'ref': 'J6, ms. 712–714, 799–1140; J9, ms. 356–358, 609–610',
}

# ---------------------------------------------------------------- Ta'wilul Ma'ani
t = read_docx('Nota Exam Tawilul Maani.docx')
S = t['sections']
tawil = {
    'id': 'tawil',
    'short': 'Ta’wilul Ma’ani',
    'title': 'Ta’wilul Ma’ani',
    'basis': 'Berdasarkan kerangka Al Fathun Nawa · Jilid 6 dan 9',
    'lead': lead(t),
    'key': {
        'q': 'Apakah yang hendak diberitahu oleh ayat ini?',
        'text': 'Memahami tujuan ayat melalui hubungan tajuk dengan keterangan yang menjelaskannya.',
    },
    'groups': [
        {
            'heading': '3 Istilah Penting',
            'compact': True,
            'items': [
                item('M', 'Mulk', 'Takluk dan arah tujuan', ''),
                item('M', 'Maudha’', 'Tajuk perbincangan', ''),
                item('K', 'Khitab', 'Isi yang menerangkan tajuk', ''),
            ],
            'details': details(S[3]),
        },
        {
            'heading': '5 Pola Asas',
            'items': [
                item(1, 'Dhomir Taqaddim', 'Satu ayat · Tajuk di hujung', 'Huraian → Tajuk', 'Al Baqarah 2:186', S[5]),
                item(2, 'Dhomir Ta’akhkhir', 'Satu ayat · Tajuk di pangkal', 'Tajuk → Huraian', 'Yusuf 12:111', S[6]),
                item(3, 'Dhomir Taqaddimul Awwal', 'Rangkaian ayat · Kesimpulan di belakang', 'Ayat penerang → Ayat kesimpulan', 'Al Baqarah 2:2–4 → 2:5', S[7]),
                item(4, 'Dhomir Taqaddimul Aakhir', 'Rangkaian ayat · Tajuk di hadapan', 'Ayat tajuk → Ayat penerang', 'Al Mukminun 23:1 → 23:2–11', S[8]),
                item(5, 'Dhomir Kulli Awla', 'Pengertian langsung keseluruhan ayat', 'Fahami kenyataan secara menyeluruh.', 'Bismillahir rahmanir rahim', S[9]),
            ],
        },
        {
            'heading': '3 Peringkat Tambahan',
            'items': [
                item(6, 'Khamsul Gharib', 'Satu soalan, lima jawapan', 'Ulang soalan yang sama 5 kali; beri 5 sudut jawapan berasas.', None, S[10]),
                item(7, 'Ra’sil ‘Ulum', 'Kata pemimpin', 'Huraikan kata pemimpin atau tokoh ilmu.', None, S[11]),
                item(8, 'Ra’sis Syahid', 'Karya pujangga', 'Huraikan mesej puisi, pantun, gurindam atau lirik.', None, S[12]),
            ],
            'note': 'Ra’sil ‘Ulum dan Ra’sis Syahid ialah peluasan kepada teks manusia; bezakan daripada ayat Al Quran.',
        },
    ],
    'steps': {'heading': 'Cara Menggunakan', 'items': ['Pilih ayat', 'Kenal pola', 'Tentukan tajuk', 'Huraikan khitab', 'Semak ayat sokongan', 'Rumuskan tujuan']},
    'formula': {
        'heading': 'Formula Ingatan',
        'chips': ['Satu ayat: hujung / pangkal', 'Rangkaian ayat: belakang / hadapan', 'Kulli: keseluruhan', 'Tambahan: 5 jawapan · kata tokoh · karya pujangga'],
    },
    'notes': {
        'heading': 'Nota',
        'items': ['Istilah dan pola mengikuti penggunaan pengarang. Kehadiran satu lafaz sahaja tidak mencukupi; semak susunan dan konteks ayat.'],
    },
    'sections': general_sections(t, [1, 2, 4, 13, 14, 15]),
    'ref': 'J6, ms. 632–705; J9, ms. 301–302, 598–601, 865–869',
}

# ---------------------------------------------------------------- Al Ashlih Asbaabun Nuzul
a = read_docx('Nota Exam Al Ashlih Asbaabun Nuzul.docx')
S = a['sections']
unsur = S[3]['paras']
assert len(unsur) == 4, 'expected four unsur paragraphs in section 3'
asbab = {
    'id': 'asbab',
    'short': 'Al Ashlih Asbaabun Nuzul',
    'title': 'Al Ashlih Asbaabun Nuzul',
    'basis': 'Berdasarkan kerangka Al Fathun Nawa · Jilid 9',
    'lead': lead(a),
    'key': {
        'label': 'Apa maksudnya?',
        'text': 'Meneliti masalah yang diisyaratkan oleh ayat, menghuraikan kesannya dan mencari penyelesaian melalui petunjuk Al Quran.',
    },
    'groups': [{
        'heading': '4 Unsur Utama',
        'items': [
            dict(item(1, 'Rentetan Peristiwa', 'Unsur pertama', 'Rangkaian keadaan atau sikap yang diisyaratkan ayat.'), details={'paras': [unsur[0]], 'refs': S[3]['refs']}),
            dict(item(2, 'Dilema', 'Unsur kedua', 'Masalah atau kekusutan yang perlu dileraikan.'), details={'paras': [unsur[1]], 'refs': S[3]['refs']}),
            dict(item(3, 'Falsafah Penyelesaian', 'Unsur ketiga', 'Prinsip dan tindakan untuk membaiki keadaan.'), details={'paras': [unsur[2]], 'refs': S[3]['refs']}),
            dict(item(4, 'Nostalgia', 'Unsur keempat', 'Kemanisan dan manfaat selepas masalah diselesaikan.'), details={'paras': [unsur[3]], 'refs': S[3]['refs']}),
        ],
    }],
    'steps': {
        'heading': '4 Langkah Asas',
        'items': ['Baca ayat dan kenal pasti kalimah dilema', 'Tentukan masalah yang dibangkitkan', 'Huraikan rentetan peristiwa tersirat', 'Jelaskan penyelesaian dan manfaatnya'],
    },
    'lists': [{
        'heading': '7 Peringkat Jawapan Exam',
        'items': ['Kepentingan ayat', 'Rentetan peristiwa tersirat', 'Dilema Tuhan dengan manusia', 'Kesan rentetan dilema', 'Jalan falsafah penyelesaian', 'Nostalgia pengashlihan', 'Rumusan: sertakan 3 ayat sokongan dan jelaskan kaitannya.'],
        'note': '“Dilema Tuhan dengan manusia” ialah istilah pengarang bagi hubungan petunjuk Tuhan dengan sikap manusia.',
    }],
    'example': {
        'heading': 'Contoh · Muhammad 47:24',
        'rows': [
            ['Isu', 'Keengganan mentadabbur Al Quran.'],
            ['Dilema', 'Hati tertutup terhadap petunjuk.'],
            ['Penyelesaian', 'Teliti ayat, fahami dan ambil pengajaran.'],
            ['Nostalgia', 'Kefahaman lebih jelas dan sikap lebih terbuka.'],
        ],
        'note': 'Contoh ini ialah ringkasan huraian, bukan petikan ayat.',
    },
    'formula': {'heading': 'Ingat', 'chips': ['Rentetan', 'Dilema', 'Penyelesaian', 'Nostalgia'], 'flow': True},
    'notes': {
        'heading': 'Nota',
        'items': ['Huraian tersirat perlu disandarkan kepada ayat; jangan dianggap sebagai bukti sejarah sebab turunnya ayat.'],
    },
    'sections': general_sections(a, [1, 2, 4, 5, 6, 7, 8, 9, 10, 11]),
    'ref': 'Jilid 9, ms. 12–19, 28–29, 34–35, 399–402',
}

notes = {'preparedBy': 'Peguam Ghazali', 'topics': [khitab, syariah, tawil, asbab]}
(ROOT / 'notes.json').write_text(json.dumps(notes, ensure_ascii=False, indent=1), encoding='utf-8')
print('Built notes.json:', ', '.join('%s (%d cards, %d sections)' % (tp['short'], sum(len(g['items']) for g in tp['groups']), len(tp['sections'])) for tp in notes['topics']))
