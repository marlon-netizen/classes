from lib import *

learn = '''
  <div class="card warm">
    <h3>Rights and duties go together</h3>
    <p>A <strong>Constitution</strong> (the Magna Carta) is the fundamental law of a country. It organizes life in society and the work of the State, and it <strong>guarantees the people their rights and freedoms</strong>. In Nicaragua it sets the limits and relations between the powers of the State (Legislative, Executive, Electoral and Judicial) and between them and the citizens.</p>
    <p style="margin:0">Human beings, <strong>just by existing</strong>, have the right to life: no one can be deprived of it for any reason. Everyone has the <b>same rights</b>, and everyone has the <b>duty to respect</b> the rights of others.</p>
  </div>
  <div class="card">
    <h3>Three groups of rights in the Constitution</h3>
    <div class="fact">
      <div><b class="h">Political rights (Arts. 47–55)</b>Take part in public life: vote and be elected, petition the authorities, assemble peacefully, join organizations and parties.</div>
      <div><b class="h">Social rights (Arts. 56–69)</b>Work, education and culture, health, a healthy environment, social security, food, housing, sport and recreation, truthful information, freedom of religion.</div>
      <div><b class="h">Family rights (Arts. 70–79)</b>Protection of the family, equal rights of all children, special protection for children, mothers and the elderly, equal responsibilities of parents, adoption in the child's interest.</div>
    </div>
  </div>
'''

ideas = [
 {"tab": "1. What is a Constitution?", "title": "The Constitution: strength of our values", "ref": "Textbook, Tema 16",
  "pts": ["It is the <b>fundamental norm</b> of a sovereign State, established or accepted to govern it.", "It sets limits and defines relations among the powers of the State and between those powers and citizens.", "Its main characteristic is <b>supremacy</b>: it is above every other law.", "It <b>seeks to guarantee the people's rights and freedoms</b> and defines the duties and rights of citizens."],
  "key": "The Constitution protects everyone's rights, and that is why we must know it."},
 {"tab": "2. Political rights", "title": "Political rights: taking part in public life", "ref": "Arts. 47–55",
  "pts": ["<b>Art. 47:</b> Nicaraguans who have turned sixteen are citizens and enjoy political rights.", "<b>Art. 48:</b> <b>Equality</b> of all Nicaraguans in political rights, duties and responsibilities, including <b>equality of man and woman</b>.", "<b>Art. 50–51:</b> Citizens take part in public affairs on equal terms and have the right to <b>elect and be elected</b>.", "<b>Art. 52:</b> The right to make petitions, report anomalies and offer constructive criticism, and to get a prompt answer.", "<b>Art. 53–55:</b> <b>Peaceful assembly</b> needs no prior permission; the right to demonstrate in accordance with the law; the right to organize or join political parties."],
  "key": "Political rights let citizens take part in decisions that affect everyone."},
 {"tab": "3. Social rights", "title": "Social rights: what we need to live with dignity", "ref": "Arts. 56–69",
  "pts": ["<b>Work</b> (Art. 57), <b>education and culture</b> (Art. 58) and <b>health</b> (Art. 59: the State organizes health programs; citizens must follow the sanitary measures).", "A <b>healthy environment</b> (Art. 60) and <b>social security</b> (Art. 61).", "<b>Protection against hunger</b> (Art. 63) and a <b>decent, safe home</b> (Art. 64).", "<b>Sport, physical education, recreation</b> (Art. 65) and <b>truthful information</b> (Art. 66).", "<b>Freedom of religion</b>: show beliefs in private or in public (Art. 69), without preventing others from exercising their rights."],
  "key": "Social rights protect the basic needs of every person."},
 {"tab": "4. Family rights", "title": "Family rights: the family is the fundamental nucleus", "ref": "Arts. 70–79",
  "pts": ["<b>Art. 70:</b> The family is the fundamental nucleus of society and has the right to be protected.", "<b>Art. 71, 75, 76:</b> Children have <b>special protection</b> and <b>equal rights</b>; the State creates programs for minors.", "<b>Art. 73:</b> Family relations rest on <b>respect, solidarity and equal rights and responsibilities</b>. Parents care for the home and the education of their children; children must respect and help their parents.", "<b>Art. 77:</b> The elderly have the right to protection from family, society and the State.", "<b>Art. 79:</b> Adoption exists in the exclusive interest of the child."],
  "key": "In the family we learn and practice rights and duties every day."},
 {"tab": "5. Dignity & equality", "title": "Dignity, equality, rights and duties", "ref": "Applying it in the classroom",
  "pts": ["<b>Dignity:</b> every person has equal worth, so no one may be humiliated or excluded.", "<b>Equality:</b> the same rights for everyone, with no discrimination.", "<b>Right + duty:</b> my right to learn comes with my duty not to disturb others' learning.", "When a right is violated, <b>name it, think about who is affected, and respond respectfully</b>; if needed, ask a responsible adult for help."],
  "key": "Defending rights starts with respect for the people next to us."},
]

vocab = [
 ["Constitution", "The fundamental law of a country (the Carta Magna)."],
 ["Sovereign", "A State that governs itself with no outside power above it."],
 ["Supremacy", "Being above everything else: the Constitution is above every other law."],
 ["Discrimination", "Treating people worse because of who they are."],
 ["Anomaly", "Something wrong or irregular that should be reported."],
 ["Rehabilitation", "Helping someone recover skills, health or a place in society."],
 ["Monopoly", "When one group controls everything in a field and others cannot take part."],
 ["Dignity", "The equal worth of every person."],
 ["Citizen", "A person with rights and duties in a country; in Nicaragua, those who have turned sixteen."],
]

examples = [
 {"title": "Example 1: Which kind of right is it?",
  "problem": "<i>“Every Nicaraguan has the right to education and culture.”</i> Is it a political, social or family right?",
  "steps": [["Ask what the right protects.", "It protects something every person needs to develop: learning."],
            ["Recall the three groups.", "Political = taking part in public life. Social = basic needs. Family = family life and protection."],
            ["Match.", "Education is a basic need."],
            ["Answer.", "It is a <b>social right</b> (Art. 58).", True]]},
 {"title": "Example 2: A case of rights in the classroom",
  "problem": "<i>A new student speaks little Spanish. Group members never give her a turn to talk and choose the tasks without asking her.</i>",
  "steps": [["1. Which right is affected?", "Her <b>dignity</b> and <b>equality</b>: she is not treated as equal. Her right to education and to take part."],
            ["2. Who is affected and how?", "She feels excluded and cannot learn with her group."],
            ["3. What duty does the group have?", "To respect her and give everyone the same chance to speak and contribute."],
            ["4. What is the respectful response?", "Invite her to speak, listen patiently, share the tasks, and tell the teacher if exclusion continues."],
            ["Answer.", "Her right to equality and participation is being ignored. The group should include her and share tasks. If it continues, ask the teacher for help.", True]]},
 {"title": "Example 3: Pair each right with a duty",
  "problem": "Art. 59 gives the right to health. Which duty goes with it?",
  "steps": [["Read the article again.", "“Citizens have the obligation to comply with the sanitary measures that are determined.”"],
            ["Find the duty.", "Following the health rules (for example, vaccination campaigns or school hygiene rules)."],
            ["Explain the link.", "Health is protected only when everyone cooperates."],
            ["Answer.", "The right to health goes with the <b>duty to follow health measures</b> that protect everyone.", True]]},
 {"title": "Example 4: Write a well-argued answer",
  "problem": "Answer in 3 sentences: <i>“A classmate is mocked for his family situation. Which right is violated and what should you do?”</i>",
  "steps": [["Sentence 1: name the right.", "“His right to dignity and equality is violated.”"],
            ["Sentence 2: give the reason.", "“Mocking someone for his family treats him as less valuable and every person has equal worth.”"],
            ["Sentence 3: say what to do.", "“I would not join the mocking, I would support him, and I would tell a teacher if it continued.”"],
            ["Check.", "Right named ✓ Reason ✓ Respectful action ✓"],
            ["Final answer.", "<i>His right to dignity and equality is violated. Mocking him treats him as less valuable, but every person has equal worth. I would not join in, I would support him and I would tell a teacher if it continued.</i>", True]]},
]

quiz = [
 Q("What is the Constitution (Carta Magna)?", ["The fundamental norm of a State that organizes it and guarantees rights", "A school rule book", "A list of holidays", "A national song"], "It is the supreme law that organizes the State and protects rights and freedoms."),
 Q("At what age do Nicaraguans become citizens with political rights?", ["Sixteen", "Twelve", "Eighteen", "Twenty-one"], "Art. 47: Nicaraguans who have turned sixteen are citizens."),
 Q("Which statement about equality is correct (Art. 48)?", ["All Nicaraguans are equal in their political rights and duties, and man and woman are absolutely equal", "Only adults have rights", "Some groups have more rights", "Equality applies only in school"], "Equality is unconditional."),
 Q("Which is a political right?", ["To elect and be elected", "To have a decent home", "To rest and play sports", "To form a family"], "Art. 51 gives the right to elect and be elected. The others are social or family rights."),
 Q("Does peaceful assembly need prior permission (Art. 53)?", ["No, it does not require prior permission", "Yes, always", "Only on weekends", "Only for adults"], "Art. 53 recognizes the right of peaceful assembly, without prior permission."),
 Q("Which is a social right?", ["The right to health", "The right to elect a president", "The right to adopt", "The right to join a party"], "Health is a social right (Art. 59)."),
 Q("Which statement about the family (Art. 70) is correct?", ["The family is the fundamental nucleus of society and has the right to protection", "The family has no legal protection", "Only large families are protected", "Families protect the State"], "Art. 70."),
 Q("According to Art. 73, family relations rest on…", ["Respect, solidarity and equal rights and responsibilities", "Obedience without questions", "Money", "Age only"], "Children must also respect and help their parents."),
 Q("According to Art. 75, children…", ["All have equal rights", "Have rights depending on their parents", "Have no rights until sixteen", "Have rights only at school"], "No discriminatory designations regarding filiation."),
 Q("Which duty goes with the right to health (Art. 59)?", ["Complying with the sanitary measures that are determined", "Avoiding every doctor", "Paying no attention to the rules", "Waiting until others act"], "Rights and duties go together."),
]

acts = [
 {"id": "act-quiz", "type": "quiz", "title": "Mastery Quiz (10 questions)", "intro": "Ten questions on the Constitution and human rights. Aim for 80% or higher.", "qs": quiz},
 {"id": "act-sort", "type": "sort", "title": "Political, Social or Family Right?", "intro": "Classify each right.",
  "choices": [{"k": "P", "label": "🗳 Political"}, {"k": "S", "label": "🏥 Social"}, {"k": "F", "label": "👪 Family"}],
  "cards": [["The right to elect and be elected.", "P", "Art. 51 (political)."], ["The right to petition authorities and get a prompt answer.", "P", "Art. 52 (political)."], ["The right of peaceful assembly.", "P", "Art. 53 (political)."],
            ["The right to education and culture.", "S", "Art. 58 (social)."], ["The right to live in a healthy environment.", "S", "Art. 60 (social)."], ["The right to sport, recreation and leisure.", "S", "Art. 65 (social)."], ["The right to truthful information.", "S", "Art. 66 (social)."],
            ["The right of the elderly to protection.", "F", "Art. 77 (family)."], ["Equal rights of all children.", "F", "Art. 75 (family)."], ["The right of adoption in the child's interest.", "F", "Art. 79 (family)."]]},
 {"id": "act-match", "type": "match", "title": "Match the Article", "intro": "Tap an article on the left, then the right it states.",
  "pairs": [["Art. 47", "Citizens: Nicaraguans who have turned sixteen"], ["Art. 48", "Equality, including man and woman"], ["Art. 52", "Petition, report anomalies, constructive criticism"], ["Art. 57", "Right to work"], ["Art. 58", "Right to education and culture"], ["Art. 61", "Social security"], ["Art. 63", "Protection against hunger"], ["Art. 64", "A decent, safe home"], ["Art. 69", "Freedom of religion"]]},
 {"id": "act-rd", "type": "sort", "title": "Right or Duty?", "intro": "Is each statement mostly a <b>right</b> or a <b>duty</b>?",
  "choices": [{"k": "R", "label": "⚖ Right"}, {"k": "D", "label": "🤝 Duty"}],
  "cards": [["Learning in a safe classroom.", "R", "Education is a right."], ["Not disturbing classmates while they learn.", "D", "Respecting others' rights is a duty."], ["Expressing my ideas respectfully.", "R", "Freedom to express ideas."],
            ["Listening to others' ideas.", "D", "Respect means listening."], ["Being treated with dignity.", "R", "Everyone's dignity must be respected."], ["Following sanitary measures that protect public health.", "D", "Art. 59 includes this obligation."],
            ["Respecting and helping my parents.", "D", "Art. 73 says children must respect and help their parents."], ["Being protected as a child.", "R", "Children enjoy special protection."]]},
 {"id": "act-multi", "type": "multi", "title": "Select All That Apply", "intro": "Some questions have more than one right answer.",
  "qs": [{"q": "Which of these are social rights?", "o": ["Health", "Education and culture", "A healthy environment", "The right to join a political party"], "a": [0, 1, 2], "e": "Joining parties is a political right (Art. 55)."},
         {"q": "Which of these are political rights?", "o": ["To petition the authorities", "To assemble peacefully", "To elect and be elected", "To a decent home"], "a": [0, 1, 2], "e": "Housing is a social right (Art. 64)."},
         {"q": "What does the Constitution do?", "o": ["Organizes the State", "Sets limits between the powers of the State", "Guarantees people's rights and freedoms", "Replaces school rules"], "a": [0, 1, 2], "e": "It is the supreme law, not a school rule book."},
         {"q": "Which actions respect other people's rights in class?", "o": ["Giving everyone a turn to speak", "Not excluding anyone", "Disagreeing politely", "Mocking someone's accent"], "a": [0, 1, 2], "e": "Mocking violates dignity and equality."}]},
 {"id": "act-seq", "type": "seq", "title": "Responding to a Rights Case", "intro": "Put the steps for responding to a case in the best order.",
  "items": [{"t": "Read the case and say what happened", "hint": "Start by understanding the facts.", "why": "Always begin with the facts."},
            {"t": "Name the right that is being affected", "hint": "Which right is at stake?", "why": "Name the right (dignity, equality, education, health…)."},
            {"t": "Think about who is affected and how", "hint": "Think about the person's feelings and needs.", "why": "Empathy helps you understand the harm."},
            {"t": "Say which duty each person has", "hint": "Everyone has duties toward others.", "why": "Rights come with duties."},
            {"t": "Choose a respectful action", "hint": "What can you do, calmly and safely?", "why": "A respectful action helps without causing new harm."},
            {"t": "Ask a responsible adult for help if the problem continues", "hint": "The last resort if it does not stop.", "why": "Teachers and family can help protect rights."}]},
 {"id": "act-cloze", "type": "cloze", "title": "Complete the Sentences", "intro": "Choose the word that completes each sentence.",
  "items": [["Nicaraguans who have turned ", ["sixteen", "ten", "thirty"], 0, " are citizens.", "Art. 47."],
            ["The Constitution is the ", ["fundamental", "optional", "oldest"], 0, " norm of the State.", "It is the supreme law."],
            ["Every person has the right to ", ["life", "luxury", "silence"], 0, " just by existing.", "No one can be deprived of life for any reason."],
            ["Family relations rest on respect, solidarity and ", ["equal", "unequal", "strict"], 0, " rights and responsibilities.", "Art. 73."],
            ["The right of peaceful assembly needs no prior ", ["permission", "ticket", "uniform"], 0, ".", "Art. 53."],
            ["Rights come with ", ["duties", "gifts", "exceptions"], 0, ".", "Everyone must respect the rights of others."]]},
 {"id": "act-scen", "type": "scenario", "title": "What Would You Do?", "intro": "Choose the best response in each situation. Think about dignity, equality and duties.",
  "steps": [{"s": "In your group, a classmate with a physical disability is always left out of the activities. What do you do?", "o": [
              {"t": "Invite them, adapt the activity so everyone can take part, and share the tasks.", "p": 2, "f": "You protect equality and participation."},
              {"t": "Ask the teacher to move them to another group.", "p": 0, "f": "That keeps the exclusion."},
              {"t": "Ask them if they want to join but do not change the plan.", "p": 1, "f": "Inviting is good; adapting is better."}]},
            {"s": "Someone shares a rumor about a classmate in a group chat. What is the best response?", "o": [
              {"t": "Do not share it, tell them it can hurt the classmate's dignity, and tell an adult if it continues.", "p": 2, "f": "You protect the classmate's dignity."},
              {"t": "Read it but do not reply.", "p": 1, "f": "Not sharing is good but staying silent lets harm continue."},
              {"t": "Forward it to see what others think.", "p": 0, "f": "Forwarding spreads the harm."}]},
            {"s": "Your class is choosing a representative. Some students want to exclude girls from running. What do you say?", "o": [
              {"t": "Remind them that equality is a right: everyone can elect and be elected.", "p": 2, "f": "Equality of man and woman is a constitutional principle."},
              {"t": "Say nothing because it is not your problem.", "p": 0, "f": "Defending equality is everyone's responsibility."},
              {"t": "Suggest a vote and accept the result even if girls cannot run.", "p": 1, "f": "A vote is fair only if everyone can take part."}]},
            {"s": "A classmate keeps talking during a test, disturbing others. Which duty is involved?", "o": [
              {"t": "The duty to respect others' right to learn: ask them kindly to be quiet and tell the teacher if needed.", "p": 2, "f": "You connect right and duty."},
              {"t": "Shout at them.", "p": 0, "f": "Shouting violates respect too."},
              {"t": "Move away silently.", "p": 1, "f": "OK, but the problem remains for others."}]}]},
 {"id": "act-case", "type": "open", "title": "My Rights Case Analysis", "rtitle": "Case analysis: a rights violation", "min": 20,
  "intro": "Read this case. <i>“In the school yard, a group of older students keeps taking the ball and does not let the younger students play. They say, ‘you are too small.’”</i> Write a well-argued answer (see Worked Example 4).",
  "prompts": [{"q": "1. Which right or rights are being violated, and why?", "rows": 3}, {"q": "2. What duty does each person have?", "rows": 3}, {"q": "3. What respectful action would you take?", "rows": 4}]},
 {"id": "act-real", "type": "open", "title": "Rights in Real Life", "rtitle": "Real-life situations (political, social, family)", "min": 15,
  "intro": "From your textbook (Tema 16): in pairs, write a real-life situation for each group of rights.",
  "prompts": [{"q": "a. Political rights: a real-life situation", "rows": 3}, {"q": "b. Social rights: a real-life situation", "rows": 3}, {"q": "c. Family rights: a real-life situation", "rows": 3}]},
 {"id": "act-book", "type": "open", "title": "Book Review Questions", "rtitle": "Review questions (Creciendo en Valores, p. 107)", "min": 20,
  "intro": "From your textbook. Answer with what you learned this week.",
  "prompts": [{"q": "1. What are social rights based on?", "rows": 3}, {"q": "2. What are family rights based on?", "rows": 3}, {"q": "3. What are political rights based on?", "rows": 3}]},
] + exit_acts(["1. Name one right from each group (political, social, family).", "2. Describe a case of violated rights and write a respectful response to it."],
              "Write about five lines about a time you saw a right respected or not respected in your family, school or community, and what you can do to defend it.")

W = dict(
  slug="gv8-q2-week-3-respect-for-human-rights", week=3, short="Respect for Human Rights",
  desc="Interactive study page for Growing in Values (8th grade, Q02 Week 3): human rights in the Constitution of Nicaragua (political, social and family rights), dignity, equality, rights and duties, with cases and practice.",
  eyebrow="Duties and rights · Human rights", title="Human Rights in the Family, School and Community",
  guiding="“What happens when a right is not respected, and what can I do about it?”",
  target="I can name and classify rights from the Constitution (political, social and family), connect each right with a duty, and give a respectful, well-argued response to a case of violated rights.",
  indicator="Shows respect for human rights in the family, school and community.",
  book="pp. 101–108", plan="Respect for human rights (S1_U2_C03)",
  learn=learn, ideas=ideas, vocab=vocab, examples=examples, acts=acts,
  method='<div class="card soft"><b>The four case questions:</b> (1) Which right is affected? (2) Who is affected and how? (3) What duty does each person have? (4) What is the respectful response?</div>',
  selfcheck=["I can classify a right as political, social or family.", "I can connect a right with a duty.", "I can explain what to do when a right is violated.", "I completed my case analysis and my exit ticket."],
  motto="Everyone's dignity is equal, and I defend it with respect.")
