from lib import *

learn = '''
  <div class="card warm">
    <h3>Respect is something we do</h3>
    <p>The law on the <strong>characteristics and use of the patriotic symbols</strong> tells us how to treat the flag and the anthem. But the law is only the minimum. Real respect is an <strong>attitude</strong>: we stand properly, sing with feeling, take care of the symbols and do not use them as a joke or as advertising.</p>
    <p style="margin:0">This week you will study the rules, practice them, and write a <b>decalogue</b> (ten rules) for the proper use of the symbols at school and online.</p>
  </div>
  <div class="card">
    <h3>The right posture</h3>
    <div class="fact">
      <div><b class="h">When the anthem is sung</b>Stand straight and still, sing with feeling, and understand each word. A hand over the heart is a respectful way to salute.<div class="fig" style="margin-top:8px">%s</div></div>
      <div><b class="h">When the flag is hoisted or lowered</b>Stop and face the flag. Remove any head covering with the right hand and keep your arms parallel to your body, or place the right hand, palm down, at the height of the heart.</div>
    </div>
  </div>
''' % hand_chest()

ideas = [
 {"tab": "1. Hoisting & lowering", "title": "Hoisting and lowering the National Flag", "ref": "Flag law, Articles 5–7",
  "pts": ["The flag is hoisted at <b>6:00 a.m.</b> and lowered at <b>6:00 p.m.</b> (Art. 5).", "It is hoisted daily at the Presidential House and at all barracks, with the corresponding honors (Art. 6).", "While it is hoisted or lowered, people nearby <b>stop and face</b> the flag. Civilians remove anything on their head with the right hand and keep their arms parallel to the body, or put the right hand, palm down, at heart height (Art. 7).", "<b>Drivers stop their vehicle;</b> civilian passengers may stay in their seat.", "On national holidays the flag must be hoisted on public buildings."],
  "key": "When the flag moves, we stop, face it and show respect with our posture."},
 {"tab": "2. Folding the flag", "title": "How to fold the flag", "ref": "A job for two people",
  "pts": ["You need <b>two people</b>.", "Take off the rope hooks and stretch the flag, then <b>shake it</b> to remove anything resting on the banner.", "Each person takes it by the two <b>end points</b>.", "Fold it <b>in two</b>, then <b>in two again</b>.", "Then fold it into <b>triangles</b> and keep folding triangles until it is completely folded."],
  "key": "Folding the flag carefully is another way to show respect."},
 {"tab": "3. Flag among other flags", "title": "Where does our flag go?", "ref": "Flag law, Articles 8–10",
  "pts": ["Honors to the National Flag are always made <b>before</b> honors to persons, and before the flags of other countries (Art. 8).", "When it is hoisted with other flags, all poles must be the <b>same height</b> and the flags the <b>same size</b> (Art. 9).", "The National Flag always takes the place of the <b>right</b>, which is the <b>left of the observer</b> (Art. 10).", "On dates of national <b>mourning</b> the flag is flown at <b>half-mast</b> with a black crêpe at the top."],
  "key": "Our flag leads: first honors, the place of the right, equal height."},
 {"tab": "4. Using the anthem", "title": "Rules for the National Anthem", "ref": "Anthem law, Articles 59–71",
  "pts": ["It is played at official ceremonies attended by the President (for example, solemn acts for Independence and the President taking office) and when the flag is hoisted or lowered in solemn acts (Arts. 59, 61).", "If a foreign anthem is also played, <b>ours is played first</b> (Art. 62). It is not played more than twice to honor the flag, or twice to honor the President (Art. 63).", "<b>Teaching the anthem is obligatory</b> in all schools, and it must be <b>sung daily at the entrance to class</b> in public and private schools and colleges (Arts. 64–65).", "Radio stations broadcast it at the start and end of their day without interference (Art. 70)."],
  "key": "The anthem belongs in schools and solemn acts; we learn it and sing it."},
 {"tab": "5. What is forbidden", "title": "What the law forbids with the anthem", "ref": "Anthem law, Articles 67 and 69",
  "pts": ["It is strictly forbidden to <b>alter the lyrics or the music</b> of the anthem, or to use it, in whole or in part, in other compositions or arrangements.", "It is forbidden to sing or play it for <b>advertising purposes</b>, or in canteens, vice dens or similar places.", "To make recordings, editions or reproductions, <b>authorization from the Ministry of the Interior</b> is required (Art. 69).", "A meme or a joke version that changes the words is therefore not respectful of the anthem."],
  "key": "The anthem is not a joke or an ad. We never change its words or use it to sell."},
 {"tab": "6. Respect online", "title": "Respecting the symbols on screens", "ref": "School acts and digital posts",
  "pts": ["Before you post a photo or video of a school act, ask: <b>does it show the flag or anthem with respect?</b>", "Do not post edited or mocking versions of the symbols or of the anthem's words.", "A caption can show respect too: say what the act commemorates and who took part.", "Remember: what you post represents you <b>and</b> your school."],
  "key": "Respect for the symbols applies in the schoolyard and on the screen."},
]

vocab = [
 ["Hoist", "To raise the flag up the pole."],
 ["Lower", "To bring the flag down from the pole (in Spanish: arriar)."],
 ["Half-mast", "The flag flown halfway down the pole as a sign of national mourning."],
 ["Mourning", "A period of public sadness after an important loss."],
 ["Decalogue", "A set of ten rules."],
 ["Article", "A numbered rule inside a law, such as Article 7 of the flag law."],
 ["Honors", "Ceremonial signs of respect given to the flag, the anthem or a person."],
 ["Authorization", "Official permission to do something."],
 ["Solemn act", "A formal and serious ceremony, such as an official commemoration."],
]

examples = [
 {"title": "Example 1: A flag ceremony at school",
  "problem": "<i>The flag is being hoisted during the morning ceremony. Some students keep talking and one wears a cap.</i> What should happen?",
  "steps": [["Recall the rule (Art. 7).", "People nearby <b>stop and face</b> the flag."],
            ["Check each behavior.", "Talking is not respectful. The cap should be removed with the right hand."],
            ["Choose the posture.", "Arms parallel to the body, or the right hand palm down at heart height."],
            ["Say it kindly.", "“Please stop talking and take off your cap. The flag is being hoisted.”"],
            ["Answer.", "Everyone stops, faces the flag, removes head coverings with the right hand and stays quiet until the ceremony ends.", True]]},
 {"title": "Example 2: Is this digital post respectful?",
  "problem": "<i>A student posts a video of the anthem with funny changed lyrics and an advertisement for a snack.</i>",
  "steps": [["Check the anthem rules.", "Art. 67: it is forbidden to <b>alter the lyrics</b> and to use the anthem for <b>advertising</b>."],
            ["Identify the problems.", "Changed lyrics (problem 1) and advertising use (problem 2)."],
            ["Think about the effect.", "It treats a symbol of the whole nation as a joke and as a sales tool."],
            ["Find a respectful alternative.", "Post the real anthem at a school act with a caption about what it means, with no ads."],
            ["Answer.", "The post is <b>not respectful</b> and breaks the law. A respectful post keeps the lyrics and does not use the anthem to sell.", True]]},
 {"title": "Example 3: Flags side by side",
  "problem": "A school event hoists the National Flag and the flag of a visiting school. Where does our flag go and how should the flags look?",
  "steps": [["Recall Art. 10.", "Our flag takes the place of the right, which is the <b>left of the observer</b>."],
            ["Recall Art. 9.", "All poles the <b>same height</b>; all flags the <b>same size</b>."],
            ["Recall Art. 8.", "Honors to the National Flag come first."],
            ["Answer.", "Our flag goes on the observer's left (the place of the right), on a pole of equal height, with equal-size flags, and receives honors first.", True]]},
 {"title": "Example 4: Write a rule for the decalogue",
  "problem": "Write one clear rule about the flag for a ten-rule decalogue.",
  "steps": [["Start with a vague idea.", "“Be nice to the flag.”"],
            ["Problem: can anyone check it?", "“Be nice” is too general."],
            ["Name the action and the moment.", "“Stop and face the flag when it is hoisted or lowered.”"],
            ["Add the reason if it fits.", "“…because the flag represents every Nicaraguan.”"],
            ["Check it.", "Clear verb ✓ Specific moment ✓ Possible to follow ✓ Based on the law or on respect ✓"],
            ["Final rule.", "<i>Stop and face the flag whenever it is hoisted or lowered, because it represents every Nicaraguan.</i>", True]]},
]

quiz = [
 Q("At what times is the National Flag hoisted and lowered?", ["6:00 a.m. and 6:00 p.m.", "8:00 a.m. and 4:00 p.m.", "12:00 noon and midnight", "Only on national holidays"], "Article 5 says it is hoisted at 6:00 a.m. and lowered at 6:00 p.m."),
 Q("What should people nearby do when the flag is hoisted or lowered?", ["Stop and face the flag", "Keep walking", "Turn their backs to it", "Take photos"], "Article 7: people stop and face the patriotic emblem."),
 Q("A civilian wearing a cap while the flag is hoisted should…", ["Remove it with the right hand and keep arms parallel to the body (or hand at the heart)", "Pull it lower", "Wear it with pride", "Hold it up high"], "Article 7 describes both postures."),
 Q("What should drivers do when the flag is hoisted or lowered nearby?", ["Stop their vehicle", "Honk", "Speed up", "Turn off the lights"], "Drivers stop; civilian passengers may remain seated."),
 Q("Where does the National Flag go when it is flown with foreign flags?", ["The place of the right (the observer's left)", "The far left", "Lower than the others", "It does not matter"], "Article 10: the place of the right, which is the left of the observer."),
 Q("When several flags are hoisted together, the poles must be…", ["The same height, with flags the same size", "Taller for the strongest country", "Any height", "Taller for the guest"], "Article 9: same height, same size."),
 Q("How many people are needed to fold the flag?", ["Two", "One", "Four", "Ten"], "Each person takes an end point; they fold in two, in two again, then into triangles."),
 Q("Which is forbidden with the National Anthem?", ["Changing its lyrics or using it for advertising", "Singing it at school", "Teaching it in class", "Playing it at a solemn act"], "Article 67 forbids altering the lyrics or music and using it for advertising."),
 Q("According to the law, how often must the anthem be sung at school?", ["Daily at the entrance to class", "Once a year", "Only in September", "Never in private schools"], "Article 65: it is sung daily at the entrance to class in all schools and colleges, public and private."),
 Q("On a day of national mourning the flag is flown…", ["At half-mast with a black crêpe", "Upside down", "Folded", "At the top with a red ribbon"], "At half-mast with a black crêpe at the top."),
]

acts = [
 {"id": "act-quiz", "type": "quiz", "title": "Mastery Quiz (10 questions)", "intro": "Ten questions about the rules for the flag and the anthem. Aim for 80% or higher.", "qs": quiz},
 {"id": "act-sort", "type": "sort", "title": "Respectful or Disrespectful?", "intro": "Is each action <b>respectful</b> or <b>disrespectful</b> toward the symbols?",
  "choices": [{"k": "R", "label": "✅ Respectful"}, {"k": "D", "label": "🚫 Disrespectful"}],
  "cards": [["Standing straight with the right hand at the heart while the anthem is sung.", "R", "A calm, respectful posture.", hand_chest()],
            ["Chatting loudly during the flag ceremony.", "D", "While the flag is hoisted we stop, face it and stay quiet."],
            ["Singing the anthem with feeling, even if your voice is not perfect.", "R", "What matters is what we feel, not how loudly or perfectly we sing."],
            ["Using the flag as a tablecloth at a picnic.", "D", "The flag is an emblem of the nation, not a household item."],
            ["Removing your cap with your right hand when the flag is lowered.", "R", "That is exactly what Article 7 describes."],
            ["Changing the words of the anthem for a funny video.", "D", "Article 67 forbids altering the lyrics."],
            ["Folding the flag carefully with a partner.", "R", "Folding with care is a form of respect."],
            ["Letting the flag touch the ground and leaving it there.", "D", "Care for the flag and store it properly."]]},
 {"id": "act-seq", "type": "seq", "title": "Folding the Flag in Order", "intro": "Put the steps for folding the National Flag in order.",
  "items": [{"t": "Get a second person to help", "hint": "Folding needs two people.", "why": "Two people are needed to fold the flag."},
            {"t": "Remove the rope hooks and stretch the flag out", "hint": "Free the flag from the pole fittings.", "why": "Unhook it and stretch it."},
            {"t": "Shake it to remove anything resting on the banner", "hint": "Clean it before you fold it.", "why": "Shake off anything that rests on the flag."},
            {"t": "Each person takes it by the two end points", "hint": "Start to fold with both holding the ends.", "why": "Hold the end points."},
            {"t": "Fold it in two, then in two again", "hint": "Two folds in half come before triangles.", "why": "First folds in two, then again in two."},
            {"t": "Fold it into triangles until it is completely folded", "hint": "The last stage forms triangles.", "why": "Keep folding triangles until the flag is fully folded."}]},
 {"id": "act-match", "type": "match", "title": "Match the Article to the Rule", "intro": "Tap an article on the left, then its rule on the right.",
  "pairs": [["Flag law, Art. 5", "Hoisted at 6:00 a.m. and lowered at 6:00 p.m."], ["Flag law, Art. 7", "People stop and face the flag; head coverings off"], ["Flag law, Art. 8", "Honors to the flag come before honors to persons"], ["Flag law, Art. 9", "Same pole height and same flag size"], ["Flag law, Art. 10", "Our flag takes the place of the right"], ["Anthem law, Art. 62", "Ours is played first when a foreign anthem is also played"], ["Anthem law, Art. 65", "Sung daily at the entrance to class in every school"], ["Anthem law, Art. 67", "No altering the lyrics and no advertising use"]]},
 {"id": "act-multi", "type": "multi", "title": "Select All That Apply", "intro": "Some questions have more than one right answer.",
  "qs": [{"q": "Which actions are correct while the flag is being hoisted?", "o": ["Stop and face the flag", "Remove a cap with the right hand", "Keep arms parallel to the body", "Run past the flag"], "a": [0, 1, 2], "e": "Stop, face the flag and show a respectful posture."},
         {"q": "Which of these are forbidden with the anthem?", "o": ["Changing its lyrics", "Using it in advertising", "Singing it in a bar or canteen", "Singing it at school"], "a": [0, 1, 2], "e": "Article 67 forbids all three. School singing is required."},
         {"q": "Which are true about the National Flag?", "o": ["It leads honors before persons", "It takes the place of the right among other flags", "It is flown at half-mast on mourning dates", "It must be smaller than foreign flags"], "a": [0, 1, 2], "e": "All flags are the same size; ours is not smaller."},
         {"q": "Which posts show respect for the symbols?", "o": ["A photo of students saluting the flag with a caption about the school act", "A video of the real anthem at a ceremony", "A message explaining what Independence Day commemorates", "A meme that mocks the anthem"], "a": [0, 1, 2], "e": "Respectful posts show and explain; mocking posts do not."}]},
 {"id": "act-digital", "type": "sort", "title": "Digital Posts: Respectful or Not?", "intro": "You are a school social-media team. Decide for each post.",
  "choices": [{"k": "Y", "label": "👍 Post it"}, {"k": "N", "label": "✋ Do not post it"}],
  "cards": [["A photo of the flag ceremony with the caption “Today we hoisted the flag together.”", "Y", "It shows the act with respect and explains it."],
            ["A video of students singing the anthem correctly at the entrance to class.", "Y", "Daily singing is required and the post shows it respectfully."],
            ["A filter that puts funny words over the anthem.", "N", "Altering the anthem is forbidden."],
            ["An ad for a school snack bar using the anthem as background music.", "N", "Advertising use of the anthem is forbidden."],
            ["A poster explaining how to fold the flag.", "Y", "It teaches respect for the flag."],
            ["A joke photo of someone wiping a table with the flag.", "N", "Treating the flag like a rag mocks the symbol."]]},
 {"id": "act-cloze", "type": "cloze", "title": "Complete the Sentences", "intro": "Choose the word that completes each sentence.",
  "items": [["The flag is hoisted at ", ["6:00 a.m.", "9:00 a.m.", "noon"], 0, ".", "Art. 5: 6:00 a.m."],
            ["At the flag ceremony, people stop and ", ["face", "ignore", "photograph"], 0, " the flag.", "People stop and face the flag."],
            ["Our flag takes the place of the ", ["right", "left", "back"], 0, " among other flags.", "The place of the right."],
            ["It is forbidden to ", ["alter", "teach", "learn"], 0, " the lyrics of the anthem.", "Article 67."],
            ["The anthem is sung daily at the ", ["entrance to class", "end of the year", "market"], 0, " in every school.", "Article 65."],
            ["On days of mourning the flag is flown at ", ["half-mast", "full height", "night"], 0, ".", "Half-mast with a black crêpe."]]},
 {"id": "act-scen", "type": "scenario", "title": "What Would You Do?", "intro": "Choose the best response in each situation.",
  "steps": [{"s": "During the anthem at school, a friend is laughing and nudging you. What do you do?", "o": [
              {"t": "Whisper that the anthem is being sung and stand straight so they follow your example.", "p": 2, "f": "You lead by example, kindly."},
              {"t": "Laugh quietly with them.", "p": 0, "f": "That joins the disrespect."},
              {"t": "Move away without saying anything.", "p": 1, "f": "You avoided it but could have helped."}]},
            {"s": "A classmate edits a video of the anthem to make it funny and asks you to share it. What do you say?", "o": [
              {"t": "“I will not share it: changing the anthem is not respectful and the law forbids it. Let's post the real one at our school act.”", "p": 2, "f": "Clear, polite and constructive."},
              {"t": "Share it but write that it is only a joke.", "p": 0, "f": "A joke does not make it respectful or legal."},
              {"t": "Ignore the message.", "p": 1, "f": "Not sharing is good, but speaking up helps others."}]},
            {"s": "You are driving with your family and you see the flag being lowered at 6:00 p.m. beside the road. What is correct?", "o": [
              {"t": "The driver stops the vehicle until the flag is lowered; civilian passengers may stay seated.", "p": 2, "f": "Exactly what Article 7 says."},
              {"t": "Keep driving but turn the music down.", "p": 1, "f": "Quiet is nice but the driver should stop."},
              {"t": "Honk to greet the flag.", "p": 0, "f": "Honking is not a sign of respect during the ceremony."}]},
            {"s": "You are in charge of the flag after a school event. What do you do?", "o": [
              {"t": "Ask a partner to help, fold it properly, and store it in a clean, safe place.", "p": 2, "f": "Folding takes two people and storing it well protects it."},
              {"t": "Roll it up quickly and put it in a bag.", "p": 1, "f": "Quick, but not the correct way."},
              {"t": "Leave it on a chair.", "p": 0, "f": "Leaving the flag around shows carelessness."}]}]},
 {"id": "act-deca", "type": "open", "title": "Our Decalogue of Respect", "rtitle": "Decalogue for the proper use of the symbols", "min": 10,
  "intro": "Write <b>ten rules</b> for using the flag and the anthem respectfully at school and online. Each rule should be clear, possible to follow and, if you can, say why. See Worked Example 4.",
  "prompts": [{"q": "Rule %d:" % i, "rows": 2} for i in range(1, 11)],
  "model": "1. Stop and face the flag whenever it is hoisted or lowered. 2. Take off any cap with the right hand. 3. Sing the anthem with feeling and understand each word. 4. Never change the lyrics of the anthem. 5. Never use the anthem or the flag to advertise. 6. Fold the flag with a partner and store it carefully. 7. Do not let the flag touch the ground. 8. Post photos of school acts with respectful captions. 9. Do not share jokes that mock the symbols. 10. Explain to others why the symbols deserve respect."},
 {"id": "act-book", "type": "open", "title": "Book Review Questions", "rtitle": "Review questions (Creciendo en Valores, p. 96)", "min": 20,
  "intro": "These are the review questions from your textbook. Answer them with what you learned this week.",
  "prompts": [{"q": "1. Which values characterize the National Anthem of Nicaragua?", "rows": 3}, {"q": "2. Why should you adopt a correct and respectful attitude when singing the National Anthem?", "rows": 3}, {"q": "3. How is the National Flag hoisted, lowered and folded?", "rows": 4}, {"q": "4. Where is the National Flag placed in relation to other flags?", "rows": 3}]},
] + exit_acts(["1. Explain one rule for hoisting or lowering the flag, and say why it matters.", "2. Which rule from your decalogue will you practice this week, and where?"],
              "Write about five lines. Did you see the flag or hear the anthem this week? How did people behave, and what will you do to show respect?")

W = dict(
  slug="gv8-q2-week-2-respect-for-the-symbols", week=2, short="Respect and Proper Use of the Symbols",
  desc="Interactive study page for Growing in Values (8th grade, Q02 Week 2): how to respect and use the flag and the national anthem, at school and online, with practice and a class decalogue.",
  eyebrow="Identity · Respect for the symbols", title="Respecting and Using the Symbols Properly",
  guiding="“How can I show respect for the flag and the anthem at school and on screen?”",
  target="I can explain the rules for hoisting, lowering, folding and placing the flag and for using the anthem, judge school acts and digital posts, and write a decalogue of respectful use.",
  indicator="Shows respect for the patriotic and national symbols in the family, the school and the community.",
  book="pp. 90–96", plan="Respect and proper use of the symbols (S1_U2_C02)",
  learn=learn, ideas=ideas, vocab=vocab, examples=examples, acts=acts,
  method='<div class="card soft"><b>The three questions for any act or post:</b> (1) Which rule applies? (2) Does the behavior follow it? (3) What would be the respectful alternative?</div>',
  selfcheck=["I can say when the flag is hoisted and lowered and how people should behave.", "I can explain how to fold the flag and where it goes among other flags.", "I can name two things the law forbids with the anthem.", "I wrote my decalogue and my exit ticket."],
  motto="Respect shows in what I do when the flag goes up.")
