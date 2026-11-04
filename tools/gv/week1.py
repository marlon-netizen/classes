from lib import *

def Q(q, o, e, svg=None, a=0):
    d = {"q": q, "o": o, "a": a, "e": e}
    if svg: d["svg"] = svg
    return d

learn = '''
  <div class="card warm">
    <h3>What is a national symbol?</h3>
    <p>Every nation chooses <strong>symbols</strong> to express what matters most about the country: a piece of its landscape, its animals and plants, or its values. Almost every country has an <strong>anthem</strong>, a <strong>flag</strong> and a <strong>coat of arms</strong>. Some also choose a flower, a tree or a bird.</p>
    <p style="margin:0">Nicaraguan citizens love their country and its symbols, <strong>because they represent us inside and outside the country</strong>. That is why it is our responsibility to feel and to show respect for them.</p>
  </div>
  <div class="card">
    <h3>Two families of symbols</h3>
    <div class="fact">
      <div><b class="h">Patriotic symbols (Símbolos Patrios)</b>The <b>Flag</b>, the <b>Coat of Arms</b> and the <b>National Anthem</b>.<div class="fig" style="margin-top:8px">%s</div></div>
      <div><b class="h">National symbols (Símbolos Nacionales)</b>The <b>Sacuanjoche</b> (flower), the <b>Madroño</b> (tree) and the <b>Guardabarranco</b> (bird).<div class="fig" style="margin-top:8px">%s%s%s</div></div>
    </div>
    <p class="ref" style="margin:10px 0 0">The drawings on this page are simplified versions of the real symbols. Compare them with the pictures in your textbook (pp. 88–95).</p>
  </div>
''' % (flag() + coat(), flower(), tree(), bird())

ideas = [
 {"tab": "1. The flag", "title": "The National Flag", "ref": "Patriotic symbol",
  "pts": ["Our flag has <b>horizontal blue, white and blue stripes</b> with the coat of arms in the center.", "It is a <b>patriotic symbol</b>: it represents the nation inside and outside the country.", "It is hoisted at <b>6:00 a.m.</b> and lowered at <b>6:00 p.m.</b>, and it is hoisted on public buildings on national holidays (Week 2 studies the rules in detail).", "Honors to the flag are always made before honors to persons."],
  "key": "The flag is the banner of the whole nation, so we treat it with respect and care."},
 {"tab": "2. Coat of arms", "title": "The Coat of Arms", "ref": "Patriotic symbol",
  "pts": ["The coat of arms (<i>Escudo de Armas</i>) is a <b>triangle</b> that shows a <b>rainbow</b>, <b>volcanoes</b> and a <b>Phrygian cap</b>.", "Around it are the words <b>República de Nicaragua – América Central</b>.", "It appears in the center of the flag and on official documents."],
  "key": "The coat of arms is a picture of who we are: our land, our liberty and our place in Central America."},
 {"tab": "3. The anthem", "title": "The National Anthem: “Salve a Ti Nicaragua”", "ref": "Patriotic symbol",
  "pts": ["The lyrics are by the poet <b>Salomón Ibarra Mayorga</b> (born in Chinandega on 8 September 1887), who entered the 1918 contest under the pen name <b>“Rómulo”</b>.", "The music is an old anonymous <b>liturgical psalm</b> from the late colonial era; a group of musicians led by <b>Luis A. Delgadillo</b> adapted the lyrics to it.", "It was sung for the first time on <b>16 December 1918</b>. The lyrics were made official by <b>Executive Decree No. 3 of 20 October 1939</b>.", "The anthem speaks of <b>peace</b> and <b>work</b>: “work is your worthy laurel and honor is your triumphal emblem.”"],
  "key": "Our anthem is a song of peace, work and honor. Each stanza reminds us of the sacrifice of our heroes."},
 {"tab": "4. Anthem history", "title": "How Nicaragua got its anthem", "ref": "Music came before words",
  "pts": ["<b>Late 1700s:</b> the Franciscan missionary Anselmo Castinove spread a religious melody among the people of Subtiava, near León.", "<b>1837:</b> that melody gained official status.", "<b>1876:</b> a melody by Carmen Vega with lyrics by F. Álvarez was imposed, but it lasted little.", "<b>1889–1893:</b> “Hermosa Soberana” (music by Alejandro Cousin) became official in September 1893.", "<b>1909:</b> the old missionary melody was used again, arranged for band.", "<b>1918:</b> President Emiliano Chamorro called a contest for the lyrics; the winning lyrics are the anthem we know."],
  "key": "Nicaragua had music for its anthem before it had official words."},
 {"tab": "5. National symbols", "title": "The Sacuanjoche, the Madroño and the Guardabarranco", "ref": "National symbols (declared in 1971)",
  "pts": ["<b>Sacuanjoche</b> (<i>Plumeria rubra</i>), the national flower, also called “flor de mayo”: bone-white with a yellow center. It was declared the national flower in 1971.", "<b>Madroño</b>, the national tree, grows on the Pacific coast. From November to February it flowers and its crown looks like a uniform white-cream mass among the green of the dry tropical forest.", "<b>Guardabarranco</b> (<i>Eumomota superciliosa</i>), the national bird: small, with short rounded wings and a long tail with two blue racket-shaped feathers. It eats mainly insects and digs its nest in a hole in the ground."],
  "key": "The national symbols show the nature of Nicaragua: its flora and fauna."},
 {"tab": "6. Why respect them?", "title": "Respect is a way of loving my country", "ref": "Attitude of the citizen",
  "pts": ["The symbols represent us <b>inside and outside</b> the country.", "When we respect them we also <b>honor ourselves</b> and enrich ourselves as people and as citizens.", "Respect is shown with <b>attitude</b>: standing properly, singing with feeling, caring for the symbols and not mocking them.", "Singing louder does not make us more patriotic; singing with <b>feeling and understanding</b> does."],
  "key": "A symbol deserves respect because of what it represents, not only because a rule says so."},
]

vocab = [
 ["Patriotism", "Love for one's homeland and the wish to serve and respect it."],
 ["Surge", "To appear or arise. (“A new official anthem surged in 1889.”)"],
 ["Melody", "The tune of a song, separate from its words."],
 ["Pseudonym", "A made-up name an author uses instead of their real name, such as “Rómulo.”"],
 ["Worthy", "Deserving respect or honor. (“Work is your worthy laurel.”)"],
 ["Attitude", "The way we think, feel and behave toward something."],
 ["Coat of arms", "The emblem of a nation: the triangle with the rainbow, the volcanoes and the Phrygian cap."],
 ["Decree", "An official order that makes something law, such as Decree No. 3 of 1939 for the anthem."],
 ["Emblem", "A symbol that stands for a country, group or idea."],
]

examples = [
 {"title": "Example 1: Patriotic or national symbol?",
  "problem": "<i>A classmate asks: “Is the Madroño a patriotic symbol or a national symbol?”</i>",
  "steps": [["Recall the two families.", "<b>Patriotic</b> = Flag, Coat of Arms, Anthem. <b>National</b> = Sacuanjoche (flower), Madroño (tree), Guardabarranco (bird)."],
            ["Ask: is it something we sing, fly or print, or a living thing from nature?", "The Madroño is a <b>tree</b>, a living part of our nature."],
            ["Match it to a family.", "Trees, flowers and birds are <b>national symbols</b>."],
            ["Add one detail as evidence.", "It grows on the Pacific coast and flowers white-cream from November to February."],
            ["Answer.", "The Madroño is a <b>national symbol</b> (the national tree).", True]]},
 {"title": "Example 2: Make a symbol fact card",
  "problem": "Build a fact card for <b>the Guardabarranco</b> with four parts: name, what it is, meaning or history, and how I can respect it.",
  "steps": [["Name and type.", "Guardabarranco (<i>Eumomota superciliosa</i>) · national symbol (national bird)."],
            ["What it is.", "A small bird with short rounded wings and a long tail with two blue racket-shaped feathers; it eats insects and nests in a hole in the ground."],
            ["Meaning or history.", "It was declared the national bird in 1971. It represents the wildlife of Nicaragua."],
            ["How I can respect it.", "Never harm birds or their nests, and speak of the national bird with pride."],
            ["Check the card.", "Four parts ✓ Facts from the textbook ✓ One action I can really do ✓"],
            ["Final card.", "<b>Guardabarranco</b> – national bird. Small, long tail with two blue rackets. Declared national bird in 1971. <i>I will protect birds and their nests.</i>", True]]},
 {"title": "Example 3: Why did the anthem take so long?",
  "problem": "Explain why Nicaragua “had music for its anthem before it had official words.”",
  "steps": [["Find the oldest fact.", "In the late 1700s a Franciscan missionary taught a religious melody near León."],
            ["Find when it became official.", "By 1837 the melody had gained official status."],
            ["Find when the words were chosen.", "In 1918 a contest chose lyrics (by Salomón Ibarra Mayorga) and adapted them to the old melody."],
            ["Compare the dates.", "Melody official in 1837; lyrics chosen in 1918. About 80 years apart."],
            ["Answer.", "The melody was already official in 1837, but the official lyrics were chosen only in the 1918 contest.", True]]},
 {"title": "Example 4: Explain why a symbol deserves respect",
  "problem": "Write 2–3 sentences that explain why the flag deserves respect. Use <b>Claim → Reason → Action</b>.",
  "steps": [["Claim.", "“The flag deserves respect.”"],
            ["Reason (what it represents).", "“Because it represents all Nicaraguans inside and outside the country.”"],
            ["Action (how I show it).", "“I stand straight when it is hoisted and I never mistreat it.”"],
            ["Check.", "Claim ✓ Reason about what it represents ✓ A concrete action ✓"],
            ["Final answer.", "<i>The flag deserves respect because it represents all Nicaraguans inside and outside the country. I show respect by standing straight when it is hoisted and by never mistreating it.</i>", True]]},
]

quiz = [
 Q("Which three are Nicaragua's patriotic symbols?", ["The Flag, the Coat of Arms and the National Anthem", "The Sacuanjoche, the Madroño and the Guardabarranco", "The Flag, the Madroño and the Anthem", "The Coat of Arms, the Sacuanjoche and the Guardabarranco"], "Patriotic symbols: Flag, Coat of Arms, Anthem. National symbols: flower, tree, bird."),
 Q("Which is the national flower?", ["The Sacuanjoche", "The Madroño", "The Guardabarranco", "The rose"], "The Sacuanjoche (Plumeria rubra), also called “flor de mayo,” was declared national flower in 1971."),
 Q("Which is the national tree?", ["The Madroño", "The Sacuanjoche", "The pine", "The Guardabarranco"], "The Madroño grows on the Pacific coast and flowers white-cream from November to February."),
 Q("Which is the national bird?", ["The Guardabarranco", "The macaw", "The Madroño", "The eagle"], "The Guardabarranco (Eumomota superciliosa) has a long tail with two blue racket-shaped feathers."),
 Q("Who wrote the lyrics of the National Anthem?", ["Salomón Ibarra Mayorga", "Luis A. Delgadillo", "Alejandro Cousin", "Emiliano Chamorro"], "He took part in the contest under the pen name “Rómulo.” Delgadillo led the musicians who adapted the lyrics to the music."),
 Q("When was the anthem sung for the first time?", ["16 December 1918", "15 September 1821", "20 October 1939", "26 February 1919"], "It was sung the day after its approval, on 16 December 1918. (20 October 1939 is the decree that made the lyrics official.)"),
 Q("Which two themes does the anthem especially mention?", ["Peace and work", "War and power", "Money and trade", "Sports and music"], "The anthem alludes to peace and work: “work is your worthy laurel.”"),
 Q("The music of the anthem comes from…", ["An old anonymous liturgical psalm from the late colonial era", "A modern pop song", "A folk dance written in 1950", "A foreign military march"], "The melody was first spread by a Franciscan missionary in the late 1700s."),
 Q("Why do we respect the national symbols?", ["Because they represent us inside and outside the country", "Only because a teacher says so", "Only on national holidays", "Because they are expensive"], "Symbols represent the nation, so respecting them is a way of loving our country."),
 Q("Which statement about singing the anthem is best?", ["Sing it with feeling and understand every word", "Sing it as loud as you can", "Sing it only if you have a good voice", "Skip it when it is hot"], "Singing louder does not make us more patriotic; feeling and understanding what we sing does."),
]

pics = [
 Q("Which symbol does this picture show?", ["The national flower (Sacuanjoche)", "The national tree (Madroño)", "The national bird (Guardabarranco)", "The Flag"], "Cream-white petals with a yellow center: the Sacuanjoche, Plumeria rubra.", flower()),
 Q("Which symbol does this picture show?", ["The national tree (Madroño)", "The national flower (Sacuanjoche)", "The Coat of Arms", "The National Anthem"], "A tree with a creamy-white crown in flower (November to February): the Madroño.", tree()),
 Q("Which symbol does this picture show?", ["The national bird (Guardabarranco)", "The national tree (Madroño)", "The Flag", "The national flower (Sacuanjoche)"], "A small bird with a long tail ending in two blue rackets: the Guardabarranco.", bird()),
 Q("What does this picture show?", ["The National Flag: blue, white, blue stripes with the coat of arms in the center", "The Coat of Arms alone", "The flag of another country", "A national symbol from nature"], "Horizontal blue-white-blue stripes with the coat of arms in the middle: the National Flag.", flag()),
 Q("Which symbol does this picture show?", ["The Coat of Arms", "The Flag", "The national tree (Madroño)", "The National Anthem"], "A ring with REPÚBLICA DE NICARAGUA – AMÉRICA CENTRAL around a triangle with volcanoes, a rainbow and a Phrygian cap: the Coat of Arms.", coat()),
 Q("This flag is flown at a school ceremony. Which family of symbols does it belong to?", ["Patriotic symbols", "National symbols", "Neither", "Only a decoration"], "The Flag is a patriotic symbol, together with the Coat of Arms and the Anthem.", flag()),
]

acts = [
 {"id": "act-quiz", "type": "quiz", "title": "Mastery Quiz (10 questions)", "intro": "Ten questions about Nicaragua's symbols. Aim for 80% or higher.", "qs": quiz},
 {"id": "act-sort", "type": "sort", "title": "Patriotic or National Symbol?",
  "intro": "Decide whether each card is a <b>patriotic</b> symbol or a <b>national</b> symbol.",
  "choices": [{"k": "P", "label": "🏛 Patriotic"}, {"k": "N", "label": "🌿 National"}],
  "cards": [["The Flag", "P", "The flag is one of the three patriotic symbols.", flag()],
            ["The Sacuanjoche", "N", "The flower is a national symbol.", flower()],
            ["The Madroño", "N", "The tree is a national symbol.", tree()],
            ["The Guardabarranco", "N", "The bird is a national symbol.", bird()],
            ["“Salve a Ti Nicaragua”", "P", "The National Anthem is a patriotic symbol.", None],
            ["The Coat of Arms", "P", "The triangle with the rainbow and the volcanoes, inside a ring with the country name, is the Coat of Arms, a patriotic symbol.", coat()],
            ["Plumeria rubra", "N", "That is the scientific name of the Sacuanjoche, the national flower.", None],
            ["Eumomota superciliosa", "N", "That is the scientific name of the Guardabarranco, the national bird.", None]]},
 {"id": "act-match", "type": "match", "title": "Match the Fact", "intro": "Tap an item on the left, then tap the fact that belongs to it.",
  "pairs": [["Salomón Ibarra Mayorga", "Wrote the lyrics of the anthem (pen name “Rómulo”)"], ["Anselmo Castinove", "Franciscan friar who spread the religious melody"], ["16 December 1918", "The anthem was sung for the first time"], ["20 October 1939", "Decree No. 3 made the lyrics official"], ["Plumeria rubra", "Scientific name of the Sacuanjoche"], ["November to February", "When the Madroño flowers"], ["Two blue racket feathers", "A feature of the Guardabarranco"]]},
 {"id": "act-seq", "type": "seq", "title": "The History of the Anthem in Order", "intro": "Put the steps in the order they happened.",
  "items": [{"t": "A Franciscan friar spreads a religious melody near León", "hint": "This is the oldest event: the late 1700s.", "why": "The melody came first, spread by a missionary."},
            {"t": "The melody gains official status (1837)", "hint": "After it was spread, it was made official.", "why": "By 1837 the melody was official."},
            {"t": "“Hermosa Soberana” becomes official (1893)", "hint": "A new anthem came after the old melody.", "why": "It was made official in September 1893."},
            {"t": "The old melody is used again, arranged for band (1909)", "hint": "Early 1900s.", "why": "In 1909 the missionary melody returned."},
            {"t": "A contest chooses the lyrics (1918)", "hint": "Led by President Emiliano Chamorro.", "why": "The winning lyrics by “Rómulo” were adapted to the old melody."},
            {"t": "The lyrics are made official by Decree No. 3 (1939)", "hint": "Twenty years after the anthem was first sung.", "why": "The decree of 20 October 1939 made “Salve a Ti Nicaragua” official."}]},
 {"id": "act-pics", "type": "quiz", "title": "Identify the Symbol", "intro": "Look at each picture (they are simplified drawings).", "qs": pics},
 {"id": "act-multi", "type": "multi", "title": "Select All That Apply", "intro": "Some questions have more than one right answer.",
  "qs": [{"q": "Which of these are patriotic symbols?", "o": ["The Flag", "The Coat of Arms", "The National Anthem", "The Madroño", "The Sacuanjoche"], "a": [0, 1, 2], "e": "The Madroño and the Sacuanjoche are national symbols."},
         {"q": "Which of these are national symbols?", "o": ["The Guardabarranco", "The Madroño", "The Sacuanjoche", "The Flag", "The Anthem"], "a": [0, 1, 2], "e": "Bird, tree and flower are the national symbols."},
         {"q": "Which facts are true about the National Anthem?", "o": ["Its title is “Salve a Ti Nicaragua”", "It speaks of peace and work", "Its lyrics were chosen in a contest in 1918", "Its lyrics were written in 2005"], "a": [0, 1, 2], "e": "The lyrics were chosen in 1918 and made official in 1939."},
         {"q": "Which show respect for the symbols?", "o": ["Standing properly while the anthem is sung", "Singing it with feeling and understanding", "Caring for the flag", "Making jokes about the anthem"], "a": [0, 1, 2], "e": "Respect is an attitude we show in what we do and say."}]},
 {"id": "act-cloze", "type": "cloze", "title": "Complete the Sentences", "intro": "Choose the word that completes each sentence.",
  "items": [["The ", ["Sacuanjoche", "Madroño", "Guardabarranco"], 0, " is Nicaragua's national flower.", "The Sacuanjoche is the national flower."],
            ["The Madroño flowers from November to ", ["February", "June", "August"], 0, ".", "It flowers between November and February."],
            ["The anthem's lyrics were written by Salomón Ibarra ", ["Mayorga", "Delgadillo", "Cousin"], 0, ".", "Ibarra Mayorga won the 1918 contest."],
            ["The anthem speaks of peace and ", ["work", "war", "wealth"], 0, ".", "“Work is your worthy laurel.”"],
            ["The flag, the coat of arms and the anthem are the ", ["patriotic", "national", "foreign"], 0, " symbols.", "They are the three patriotic symbols."],
            ["We respect the symbols because they ", ["represent", "replace", "forbid"], 0, " us inside and outside the country.", "Symbols represent the nation."]]},
 {"id": "act-scen", "type": "scenario", "title": "What Would You Do?", "intro": "Choose the best response in each situation. Think about respect.",
  "steps": [{"s": "A visiting student asks you what the Sacuanjoche is and why it matters. What do you say?", "o": [
              {"t": "It is our national flower (Plumeria rubra), bone-white with a yellow center. It is a national symbol that shows the nature of Nicaragua.", "p": 2, "f": "You answered clearly, with facts and the meaning."},
              {"t": "It is a flower. I think it is pretty.", "p": 1, "f": "True, but it leaves out why it is a symbol."},
              {"t": "I do not know and it does not matter.", "p": 0, "f": "Symbols matter because they represent us."}]},
            {"s": "During the anthem, a classmate starts joking and imitating a bad singer. What is the best response?", "o": [
              {"t": "Quietly remind them that the anthem is a symbol of our country and ask them to join in with respect.", "p": 2, "f": "Respectful and honest: it shows leadership without humiliating anyone."},
              {"t": "Laugh a little too, so they do not feel bad.", "p": 0, "f": "Laughing supports the disrespect."},
              {"t": "Ignore it and say nothing.", "p": 1, "f": "You did not join in, but you could have helped the group."}]},
            {"s": "For a class project, a friend wants to draw a funny cartoon on a copy of the flag. What do you suggest?", "o": [
              {"t": "Make the project about the flag's history and keep the flag itself drawn correctly and with care.", "p": 2, "f": "You still do a creative project while respecting the symbol."},
              {"t": "Let them, because it is only a drawing.", "p": 0, "f": "Mocking a symbol does not show respect."},
              {"t": "Tell them to ask the teacher but do not give any ideas.", "p": 1, "f": "Asking is good; offering an idea is better."}]},
            {"s": "You see a flag left on the ground after a school event. What do you do?", "o": [
              {"t": "Pick it up carefully, keep it from touching the ground, and give it to a teacher to store properly.", "p": 2, "f": "You cared for the symbol right away."},
              {"t": "Leave it for someone else.", "p": 0, "f": "Caring for symbols is everyone's responsibility."},
              {"t": "Tell a friend to pick it up.", "p": 1, "f": "You noticed, but you can act yourself."}]}]},
 {"id": "act-card", "type": "open", "title": "My Symbol Fact Card", "rtitle": "Symbol fact card", "min": 15,
  "intro": "Choose <b>one</b> symbol (flag, coat of arms, anthem, Sacuanjoche, Madroño or Guardabarranco) and complete its fact card. See Worked Example 2.",
  "prompts": [{"q": "1. My symbol and its type (patriotic or national):", "rows": 2},
              {"q": "2. What it is and what it looks like or says:", "rows": 3},
              {"q": "3. Its history or meaning (use facts from this page or your textbook):", "rows": 4},
              {"q": "4. One concrete way I can respect and care for it:", "rows": 3}],
  "model": "<b>Guardabarranco</b> – national symbol (national bird). A small bird with short rounded wings and a long tail with two blue racket-shaped feathers. It eats insects and digs its nest in the ground. It was declared the national bird in 1971. I will respect it by never harming birds or nests."},
 {"id": "act-reflect", "type": "open", "reflect": True, "title": "Five-Line Reflection", "rtitle": "Reflection", "min": 25, "who": True,
  "intro": "Apply what you learned at home or at school. Write about a time you saw a national symbol, or about an action you will take.",
  "prompts": [{"q": "Where did you see (or will you see) one of Nicaragua's symbols this week, and how did people treat it? Write about five lines.", "rows": 6}]},
 {"id": "act-exit", "type": "open", "reflect": True, "title": "Exit Ticket", "rtitle": "Exit ticket", "min": 20, "who": True,
  "intro": "Answer in your own words before you leave this page.",
  "prompts": [{"q": "1. Name one patriotic symbol and one national symbol, and say what each one is.", "rows": 3},
              {"q": "2. Explain why <b>one</b> of these symbols deserves respect.", "rows": 4}]},
]

W = dict(
  slug="gv8-q2-week-1-patriotic-national-symbols", week=1, short="Patriotic and National Symbols",
  desc="Interactive study page for Growing in Values (8th grade, Q02 Week 1): Nicaragua's patriotic and national symbols, their meaning and history, with worked examples and practice.",
  eyebrow="Identity · Patriotic and national symbols", title="The Symbols That Represent Nicaragua",
  guiding="“Why do the symbols of my country deserve my respect?”",
  target="I can name Nicaragua's patriotic and national symbols, explain what each one means and a key fact about its history, and say why each one deserves respect.",
  indicator="Shows respect for the patriotic and national symbols in the family, the school and the community.",
  book="pp. 88–96", plan="Patriotic and national symbols: meaning (S1_U2_C01)",
  learn=learn, ideas=ideas, vocab=vocab, examples=examples, acts=acts,
  method='<div class="card soft"><b>Symbol fact card:</b> (1) Name and type · (2) What it is · (3) History or meaning · (4) How I can respect it.</div>',
  selfcheck=["I can name the three patriotic symbols and the three national symbols.", "I can give one fact about the history of the anthem.", "I can explain why a symbol deserves respect.", "I completed my symbol fact card and my exit ticket."],
  motto="I respect my symbols because I love my country.")
