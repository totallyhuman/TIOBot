import requests
import zlib

from literate_banana import Bot

LANGUAGES = {
	'c': 'c-gcc',
	'c#': 'cs-core',
	'c++': 'cpp-gcc',
	'common lisp': 'clisp',
	'haskell': 'haskell',
	'java': 'java-openjdk9',
	'java 8': 'java-openjdk',
	'java 9': 'java-openjdk9',
	'kotlin': 'kotlin',
	'lisp': 'clisp',
	'perl': 'perl6',
	'perl 5': 'perl5',
	'perl 6': 'perl6',
	'python': 'python3',
	'python 2': 'python2',
	'python 3': 'python3',
	'ruby': 'ruby'
}

LANGLIST = [
	'C',
	'C#',
	'C++',
	'Common Lisp',
	'Haskell',
	'Java 8',
	'Java 9',
	'Kotlin',
	'Perl 5',
	'Perl 6',
	'Python 2',
	'Python 3',
	'Ruby'
]

def execute(match, trigger):
	req = bytes('Vlang\x001\x00{}\x00F.code.tio\x00{}\x00{}R'.format(
		LANGUAGES[match[0].lower()], len(match[1]), match[1]), 'utf-8')
	req = zlib.compress(req)[2:-4]
	
	res = requests.post('https://tio.run/cgi-bin/run/api/', req).text
	res = res.split(res[:16])[1:]
	
	return ['Output:\n' + res[0], 'Debug:\n' + res[1]]

def list_languages(match, trigger):
	return '\n'.join(LANGLIST)

TIOBot = Bot(
	nick = 'TIOBot',
	room = 'xkcd',
	short_help = 'I allow easy execution of code online!',
	long_help = ('I allow easy execution of code online!\n'
				 '\n'
				 'Commands:\n'
				 '    !execute [language] | [code] -> The STDOUT and STDERR output after'
				 ' execution of [code] in [language].\n'
				 '    !languages -> List of languages that I support.\n'
				 '\n'
				 'by totallyhuman'
	),
	generic_ping = 'Pong!',
	specific_ping = 'Pong!',
	regexes = {
		r'(?i)^\s*!execute\s+(.+?)\s*--\s*([\s\S]+?)\s*$': execute,
		r'(?i)^\s*!languages\s*$': list_languages
	}
)

while True:
	TIOBot.receive()
