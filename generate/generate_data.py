ENTRIES_COUNT = 1000
AUTHORS_COUNT = ENTRIES_COUNT / 7
TAGS_COUNT = None               # filled in by generate_tags
TAGS_CHOICES = None
AVERAGE_ENTRIES_PER_DAY = 5



from cStringIO import StringIO
from django.template.defaultfilters import slugify
import csv
import datetime
import os
import random

def get_writer(model):
    return csv.writer(open(model + '.csv', 'w'))

def generate_authors():
    first = [ w.strip() for w in file('firstnames.txt').readlines() ]
    last = [ w.strip() for w in file('lastnames.txt').readlines() ]
    emails = set()
    count = AUTHORS_COUNT
    authors = get_writer('authors')
    while count > 0:
        f, l = random.choice(first), random.choice(last)
        name = '%s %s' % (f, l)
        f, l = [s.lower() for s in (f, l)]
        email = '%s@%s.com' % (f, l)
        if email in emails:
            email = '%s.%s@example.com' % (f, l)
        if email in emails:
            email = '%s.%s@example.com' % (l, f)

        if email not in emails:
            emails.add(email)
            authors.writerow([AUTHORS_COUNT - count + 1, name, email])
            count -= 1

def generate_tags():
    global TAGS_COUNT, TAGS_CHOICES
    tags = get_writer('tags')
    for i, tag in enumerate(w.strip() for w in file('tags.txt').readlines()):
        tags.writerow([i+1, tag, tag])
    TAGS_COUNT = i + 1
    TAGS_CHOICES = range(1, i + 2)

def find_files(dir_path):
    return [ os.path.join(dir_path, name)
             for name in os.listdir(dir_path)
             if name.startswith('pg') and os.path.isfile(name) ]

def get_paragraphs(file_path):
    # Ignore Gutenberg file's meta-text
    HEADER, BUFFER, PARAGRAPHS = True, StringIO(), list()
    for line in file(file_path):
        if HEADER:
            if line.startswith('*** START OF THIS PROJECT GUTENBERG EBOOK'):
                HEADER = False
            continue
        if line.startswith('*** END OF THIS PROJECT GUTENBERG EBOOK'):
            break
        line = line.strip()
        if not line:
            paragraph = BUFFER.getvalue().strip()
            BUFFER = StringIO()
            if len(paragraph.split()) > 10:
                PARAGRAPHS.append(paragraph)
        else:
            BUFFER.write(line)
            BUFFER.write('\n')
    return PARAGRAPHS

def generate_text(dir_path):
    entries = ENTRIES_COUNT

    paragraphs = list()
    for file_path in find_files(dir_path):
        paragraphs.extend(get_paragraphs(file_path))

    LENGTH_CHOICES = range(3, 8)
    next_para = 0
    total_paras = len(paragraphs)
    random.shuffle(paragraphs)

    while entries > 0:
        n = random.choice(LENGTH_CHOICES)
        entry = paragraphs[next_para:next_para+n]
        if next_para + n > total_paras:
            end = next_para + n - total_paras
            random.shuffle(paragraphs)
            entry.extend(paragraphs[0:end])
            next_para = end
        else:
            next_para = next_para + n
        entry =  '\n<p>\n'.join(entry)
        title = ' '.join(entry[:40].split()[:5])
        title = title.replace('"', '').replace("'", '')

        entries -= 1
        yield title, entry

def generate_dates():
    start = datetime.datetime.now() - \
        datetime.timedelta(days=ENTRIES_COUNT / AVERAGE_ENTRIES_PER_DAY)
    time_between_entries = 1. / AVERAGE_ENTRIES_PER_DAY
    if time_between_entries > 1:
        delta = datetime.timedelta(days=time_between_entries)
    else:
        delta = datetime.timedelta(seconds=time_between_entries * 24 * 60 * 60)
    date = start
    while True:
        date += delta
        yield date

slugs = set()
def get_slug(title):
    prefix = slugify(title)
    suffix = ''
    slug = prefix
    while slug in slugs:
        suffix = int(random.random() * 1000)
        slug = '%s-%d' % (prefix, suffix)
    slugs.add(slug)
    return slug

def generate_entries():
    import sys
    path = os.path.abspath(__file__ if len(sys.argv) == 1 else sys.argv[1])
    path = path if os.path.isdir(path) else os.path.dirname(path)

    text = generate_text(path)
    dates = generate_dates()

    entry_id = 0
    tags_id = 0
    entries = get_writer('entries')
    tags = get_writer('entries_tags')
    for (title, entry), date in zip(text, dates):
        entry_id += 1
        author = random.randint(1, AUTHORS_COUNT)
        slug = get_slug(title)
        entries.writerow([entry_id, author, date, title, slug, entry])

        n = random.choice(range(3, 8))
        for tag in random.sample(TAGS_CHOICES, n):
            tags_id += 1
            tags.writerow([tags_id, entry_id, tag])

def main():
    generate_authors()
    generate_tags()
    generate_entries()

if __name__ == '__main__':
    main()
