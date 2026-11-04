from lib import *

learn = '''
  <div class="card warm">
    <h3>Signs speak a language everyone can read</h3>
    <p><strong>Traffic signs</strong> communicate messages that tell pedestrians and drivers the correct and safe way to travel on public roads. Their <b>shape and color</b> tell us what kind of message it is, even before we read the symbol.</p>
    <p style="margin:0">Cyclists must also follow the rules. <em>“Take care of your life, protect yourself, use the helmet.”</em> (textbook, p. 125)</p>
  </div>
  <div class="card">
    <h3>The three kinds of vertical signs</h3>
    <div class="fact">
      <div><b class="h">Preventive (warning)</b>Diamond shape, black symbol on a yellow background. They warn drivers that there is <b>danger</b> on the road.<div class="fig" style="margin-top:8px">%s%s</div></div>
      <div><b class="h">Regulatory</b>Circular, black symbol, white background and a red border. They state <b>limits and prohibitions</b>. Not obeying them is an infraction.<div class="fig" style="margin-top:8px">%s%s</div></div>
      <div><b class="h">Informative</b>Rectangular, blue or green background with a white frame. They <b>identify roads and guide</b> the driver and give useful data for the trip.<div class="fig" style="margin-top:8px">%s%s</div></div>
    </div>
    <p class="ref" style="margin:10px 0 0">Simplified drawings. Look for the real signs on your way to school.</p>
  </div>
''' % (kids(), curve(), speed(30), no_parking(), hospital(), airport())

ideas = [
 {"tab": "1. Preventive signs", "title": "Preventive (warning) signs", "ref": "Textbook, p. 124",
  "pts": ["<b>Shape:</b> diamond. <b>Colors:</b> yellow background, black symbol.", "They tell drivers there is a <b>danger</b> ahead (for example children crossing, a curve in the road).", "When you see one, <b>slow down and be alert</b>."],
  "key": "A yellow diamond says: be careful, danger ahead."},
 {"tab": "2. Regulatory signs", "title": "Regulatory signs", "ref": "Textbook, p. 124",
  "pts": ["<b>Shape:</b> circle. <b>Colors:</b> white background, red border, black symbol.", "They indicate <b>limitations and prohibitions</b> (for example a speed limit or no parking).", "If we do not respect them we commit an <b>infraction</b>."],
  "key": "A white circle with a red border says: this is a rule."},
 {"tab": "3. Informative signs", "title": "Informative signs", "ref": "Textbook, p. 124",
  "pts": ["<b>Shape:</b> rectangle. <b>Colors:</b> blue or green background with a white frame.", "They <b>identify roads and guide</b> the driver and give useful information for the journey (for example a hospital, an airport, a wheelchair-accessible place).", "They do not warn of danger or give an order; they <b>inform</b>."],
  "key": "A blue or green rectangle says: here is some useful information."},
 {"tab": "4. Helmet", "title": "The cyclist's helmet", "ref": "Textbook, pp. 124–125",
  "pts": ["Riding a bike is not just pedaling: there are rules and precautions.", "The most basic safety measure is the <b>helmet</b>.", "A badly given blow to the skull can cause serious injuries that affect our <b>thinking and movement</b>. That is why the helmet is important.", "<i>“Take care of your life, protect yourself, use the helmet.”</i>"],
  "key": "Protecting the head is a basic safety measure for every cyclist."},
 {"tab": "5. Cyclist rules", "title": "Rules for riding a bicycle", "ref": "Textbook, pp. 125–126",
  "pts": ["Travel on the roadway <b>in the direction of traffic</b>, never against it. Use the <b>cycle path</b> if there is one.", "Ride on the right and <b>signal</b> before turning left, turning right or braking.", "Be <b>visible</b>: light clothes and reflective materials; <b>white light in front and red light at the back</b>.", "Always use the helmet. Do not drink alcohol before riding. Avoid carrying passengers or heavy loads, zigzagging or doing stunts.", "Do not hold on to another vehicle. Do not use headphones.", "Look at the pavement for holes and slippery spots; brake carefully when wet; keep a safe distance; keep brakes in good condition.", "Respect all signs: stop at red and give priority to pedestrians."],
  "key": "A responsible cyclist is visible, predictable and protected."},
 {"tab": "6. BRET", "title": "Student Traffic Regulating Brigades (BRET)", "ref": "Textbook, pp. 126–127",
  "pts": ["The BRET exist to <b>protect the school community</b> from the risks of traffic around the school.", "Members share with other students what they learned about <b>safety, prevention and self-care</b>.", "They help protect students when they <b>enter and leave school</b> and cooperate in traffic control and pedestrian crossing near the school.", "They are important for <b>road education</b> in the school."],
  "key": "Students can lead road safety in their own school."},
]

vocab = [
 ["Preventive", "Warning: it tells you to prevent a danger."],
 ["Regulatory", "Sets a rule: a limit or a prohibition."],
 ["Informative", "Gives useful information, like a place or a direction."],
 ["Travel (transitar)", "To move along streets and roads."],
 ["Injury", "Harm to the body, such as a wound or a fracture."],
 ["Protection", "Something that keeps you safe from harm."],
 ["Infraction", "Breaking a rule or law."],
 ["Cycle path", "A lane or route made for bicycles."],
 ["Reflective", "Material that bounces light back so you can be seen at night."],
]

examples = [
 {"title": "Example 1: Name the category of a sign",
  "problem": "You see a <b>yellow diamond</b> sign with two children. What kind of sign is it and what should you do?",
  "steps": [["Read the shape and color.", "Diamond, yellow background, black symbol."],
            ["Recall the categories.", "Diamond + yellow = <b>preventive</b> (warning)."],
            ["Read the symbol.", "Children crossing: there may be a school nearby."],
            ["Answer.", "It is a <b>preventive sign</b>. Slow down and be ready to stop.", True]]},
 {"title": "Example 2: A cyclist's checklist",
  "problem": "<i>You will ride your bicycle to a friend's house at dusk.</i> What do you check before leaving?",
  "steps": [["Protect your head.", "Put on a helmet that fits."],
            ["Be seen.", "Light or reflective clothes, reflectors, <b>white light in front and red at the back</b>."],
            ["Check the bike.", "Brakes work; tires are in good condition."],
            ["Choose the route.", "Use the cycle path if there is one; otherwise ride on the right, in the direction of traffic."],
            ["Plan your signals.", "Signal before turning left, turning right and braking."],
            ["Answer.", "Helmet ✓ Visible ✓ Brakes ✓ Right route ✓ Signals ✓ No headphones ✓", True]]},
 {"title": "Example 3: A rule or a warning?",
  "problem": "Is a round sign with a white background, a red border and the number 30 a warning, a rule or information?",
  "steps": [["Shape and color.", "Circle, white background, red border."],
            ["Which category?", "<b>Regulatory</b>."],
            ["What does it do?", "It sets a limit: the speed limit."],
            ["What if we ignore it?", "It is an <b>infraction</b> and it is dangerous."],
            ["Answer.", "A <b>rule</b> (regulatory sign): do not go faster than the limit.", True]]},
 {"title": "Example 4: Design an informative sign",
  "problem": "Design an informative sign for your school and explain the safe behavior it teaches.",
  "steps": [["Choose the message.", "“Pedestrian crossing: look left, right and left.”"],
            ["Pick the category.", "It informs and guides: <b>informative</b>."],
            ["Choose shape and color.", "Rectangle, blue background, white frame."],
            ["Add the symbol.", "A simple figure of a person walking, with an arrow."],
            ["Explain the behavior.", "Cross only at the crossing and look three times."],
            ["Final design.", "<i>Blue rectangle with a white frame and a walking figure. Safe behavior: use the crossing and look left, right and left again.</i>", True]]},
]

quiz = [
 Q("What shape and color are preventive signs?", ["Diamond, yellow background, black symbol", "Circle, white background, red border", "Rectangle, blue background", "Triangle, green background"], "Preventive signs warn of danger."),
 Q("What do regulatory signs indicate?", ["Limitations and prohibitions", "Places to eat", "Useful trip information only", "Weather"], "If we do not respect them we commit an infraction."),
 Q("What shape and color are informative signs?", ["Rectangle, blue or green background, white frame", "Diamond, yellow", "Circle, red border", "Octagon, red"], "They guide and inform."),
 Q("Which sign says: be careful, there may be children crossing?", ["A yellow diamond", "A blue rectangle", "A white circle with a red border", "A green square"], "A preventive sign.", kids()),
 Q("What is the most basic safety measure for a cyclist?", ["The helmet", "A loud horn", "A backpack", "Headphones"], "A helmet protects the head from serious injury."),
 Q("In which direction should a cyclist travel on the roadway?", ["In the direction of traffic", "Against traffic", "In the middle of the road", "On the sidewalk crowded with people"], "Never against traffic; use the cycle path if there is one."),
 Q("Which lights should a bicycle have?", ["White in front and red at the back", "Red in front and white at the back", "Blue on both sides", "No lights"], "Regulation lights: white in front, red at the back."),
 Q("Why should cyclists not use headphones?", ["They reduce hearing and attention", "They are too heavy", "They are expensive", "They damage the bike"], "Cyclists must hear traffic."),
 Q("What is the BRET?", ["The Student Traffic Regulating Brigades", "A kind of traffic sign", "A cycling race", "A helmet brand"], "BRET help protect students near schools and spread road education."),
 Q("What does a cyclist do before turning left, turning right or braking?", ["Signal", "Speed up", "Close the eyes", "Honk"], "Signals tell others what you will do."),
]

acts = [
 {"id": "act-quiz", "type": "quiz", "title": "Mastery Quiz (10 questions)", "intro": "Ten questions about signs and cyclist safety. Aim for 80% or higher.", "qs": quiz},
 {"id": "act-signs", "type": "sort", "title": "Sign Categories", "intro": "Look at each sign: is it <b>preventive</b> (warning), <b>regulatory</b> (rule) or <b>informative</b> (information)? (Simplified drawings.)",
  "choices": [{"k": "P", "label": "⚠ Preventive"}, {"k": "R", "label": "⛔ Regulatory"}, {"k": "I", "label": "ℹ Informative"}],
  "cards": [["Sign 1", "P", "Yellow diamond: preventive (children crossing).", kids()], ["Sign 2", "P", "Yellow diamond: preventive (winding road ahead).", curve()], ["Sign 3", "R", "White circle with a red border: regulatory (speed limit).", speed(30)],
            ["Sign 4", "R", "White circle with a red border: regulatory (no parking).", no_parking()], ["Sign 5", "R", "White circle with a red border: regulatory (bicycles prohibited).", no_bikes()], ["Sign 6", "I", "Blue rectangle: informative (hospital).", hospital()],
            ["Sign 7", "I", "Blue rectangle: informative (airport).", airport()], ["Sign 8", "I", "Blue rectangle: informative (wheelchair-accessible place).", wheelchair()], ["Sign 9", "I", "Blue rectangle: informative (bicycle path).", bike_lane()]]},
 {"id": "act-read", "type": "quiz", "title": "What Does It Mean?", "intro": "Read each sign and choose its meaning.",
  "qs": [Q("What does this sign mean?", ["Danger: children may be crossing; slow down", "Hospital ahead", "No parking", "Speed limit"], "Yellow diamond with children: preventive.", kids()),
         Q("What does this sign mean?", ["Danger: the road winds ahead; slow down", "Children crossing", "Airport", "No entry"], "A winding road: preventive.", curve()),
         Q("What does this sign mean?", ["Do not go faster than 30", "Minimum speed 30", "Parking for 30 cars", "30 minutes of rest"], "A regulatory speed limit.", speed(30)),
         Q("What does this sign mean?", ["Parking is not allowed here", "Parking is available", "Taxi stop", "A parking garage is near"], "A regulatory prohibition.", no_parking()),
         Q("What does this sign mean?", ["Bicycles are not allowed", "Bike lane", "Bike for rent", "Bike repair"], "A regulatory prohibition.", no_bikes()),
         Q("What does this sign tell you?", ["There is a hospital nearby", "Parking is forbidden", "Danger ahead", "School zone"], "An informative sign.", hospital()),
         Q("What does this sign tell you?", ["The way to the airport", "Parking is forbidden", "Danger ahead", "Children crossing"], "An informative sign.", airport())]},
 {"id": "act-match", "type": "match", "title": "Match the Sign Type", "intro": "Tap the feature on the left, then the sign type.",
  "pairs": [["Diamond, yellow background", "Preventive sign"], ["Circle, white background, red border", "Regulatory sign"], ["Rectangle, blue or green background", "Informative sign"], ["Warns of danger on the road", "Preventive sign (purpose)"], ["Sets limits and prohibitions", "Regulatory sign (purpose)"], ["Guides and gives trip data", "Informative sign (purpose)"]]},
 {"id": "act-cyc", "type": "sort", "title": "Cyclist: Safe or Risky?", "intro": "Is each cyclist behavior <b>safe</b> or <b>risky</b>?",
  "choices": [{"k": "S", "label": "🟢 Safe"}, {"k": "R", "label": "🔴 Risky"}],
  "cards": [["Wearing a helmet that fits on every ride.", "S", "The helmet protects the head.", helmet()], ["Riding against the direction of traffic.", "R", "Always travel in the direction of traffic."], ["Using a white front light and a red rear light at night.", "S", "Visibility is key."],
            ["Listening to music with headphones while riding.", "R", "Headphones reduce hearing and attention."], ["Holding on to a moving truck to go faster.", "R", "Never hold on to another vehicle."], ["Signaling before turning left.", "S", "Signals tell others your plan."],
            ["Zigzagging between cars to impress friends.", "R", "Stunts destabilize you and endanger others."], ["Slowing down and braking carefully on wet pavement.", "S", "Wet pavement is slippery."], ["Checking that the brakes work before leaving.", "S", "Keep the bicycle in good condition."], ["Carrying a friend on the handlebars.", "R", "Avoid carrying passengers."]]},
 {"id": "act-multi", "type": "multi", "title": "Select All That Apply", "intro": "Some questions have more than one right answer.",
  "qs": [{"q": "Which make a cyclist more visible?", "o": ["Light or reflective clothes", "White front light", "Red rear light", "Dark clothes at night"], "a": [0, 1, 2], "e": "Dark clothes at night make you hard to see."},
         {"q": "Which are regulatory signs?", "o": ["Speed limit", "No parking", "Bicycles prohibited", "Hospital"], "a": [0, 1, 2], "e": "The hospital sign is informative."},
         {"q": "What are the tasks of the BRET?", "o": ["Help students enter and leave school safely", "Share what they learned about safety and prevention", "Cooperate in traffic control near the school", "Fine drivers"], "a": [0, 1, 2], "e": "The BRET are students, not police."},
         {"q": "Which should a cyclist avoid?", "o": ["Zigzagging", "Carrying heavy loads", "Using headphones", "Using a cycle path"], "a": [0, 1, 2], "e": "Cycle paths are the safest place to ride."}]},
 {"id": "act-seq", "type": "seq", "title": "Getting Ready for a Safe Ride", "intro": "Put the steps in the best order before you start to ride.",
  "items": [{"t": "Check that the brakes and tires are in good condition", "hint": "Check the bike before anything else.", "why": "A bike in good condition is the base of a safe ride."},
            {"t": "Put on a helmet that fits", "hint": "Protect the head.", "why": "The helmet is the most basic safety measure."},
            {"t": "Put on light or reflective clothes and turn on the lights", "hint": "Make yourself visible.", "why": "White light in front, red at the back."},
            {"t": "Choose the cycle path or the right side of the roadway", "hint": "Choose where to ride.", "why": "Use the cycle path if there is one."},
            {"t": "Signal before you turn or brake", "hint": "While riding.", "why": "Signals tell others your plan."},
            {"t": "Stop at red lights and give way to pedestrians", "hint": "When you reach a crossing.", "why": "Respect signs and pedestrian priority."}]},
 {"id": "act-cloze", "type": "cloze", "title": "Complete the Sentences", "intro": "Choose the word that completes each sentence.",
  "items": [["Preventive signs are ", ["yellow", "green", "red"], 0, " diamonds.", "Yellow diamond, black symbol."],
            ["Regulatory signs have a white background and a ", ["red", "blue", "green"], 0, " border.", "They set limits and prohibitions."],
            ["Informative signs are ", ["rectangular", "round", "triangular"], 0, " with a blue or green background.", "They inform and guide."],
            ["A cyclist should travel in the ", ["direction", "opposite", "middle"], 0, " of traffic.", "Never against traffic."],
            ["Bicycles should have a white light in front and a ", ["red", "blue", "yellow"], 0, " light at the back.", "Regulation lights."],
            ["The BRET help protect ", ["students", "tourists", "drivers"], 0, " near schools.", "Student Traffic Regulating Brigades."]]},
 {"id": "act-scen", "type": "scenario", "title": "What Would You Do?", "intro": "Choose the best response in each situation.",
  "steps": [{"s": "Your friends ride bikes without helmets because “nothing ever happens.” What do you do?", "o": [
              {"t": "Wear yours and explain that a blow to the head can cause serious injuries that affect thinking and movement.", "p": 2, "f": "You set an example and give a reason."},
              {"t": "Take yours off to fit in.", "p": 0, "f": "Peer pressure is not a reason to risk your head."},
              {"t": "Wear it but say nothing.", "p": 1, "f": "Good for you, but you could help them too."}]},
            {"s": "You see a yellow diamond sign with a curve ahead while riding. What is the best response?", "o": [
              {"t": "Slow down, stay on the right and be ready for the curve.", "p": 2, "f": "A preventive sign asks us to be careful."},
              {"t": "Speed up to pass the curve quickly.", "p": 0, "f": "Speeding on a curve is dangerous."},
              {"t": "Ignore it because it is not a rule.", "p": 1, "f": "It is a warning; it is smart to follow it."}]},
            {"s": "It is getting dark and your bike has no lights. What do you do?", "o": [
              {"t": "Do not ride until you have the white front and red rear lights and reflective clothes, or ask an adult to take you.", "p": 2, "f": "Being visible is part of safety."},
              {"t": "Ride fast to get there before it is dark.", "p": 0, "f": "Speed does not replace visibility."},
              {"t": "Ride very carefully on the road.", "p": 1, "f": "Careful is good but you will still be hard to see."}]},
            {"s": "You are a BRET member at the school gate and a student runs to cross outside the crossing. What do you do?", "o": [
              {"t": "Stop them kindly, guide them to the crossing and remind them of the three looks.", "p": 2, "f": "You use your training to protect them."},
              {"t": "Shout at them from far away.", "p": 1, "f": "Calling attention helps, but guiding is better."},
              {"t": "Ignore it because the traffic is slow.", "p": 0, "f": "Even slow traffic is risky."}]}]},
 {"id": "act-design", "type": "open", "title": "Design a Sign", "rtitle": "Sign design and the safe behavior it teaches", "min": 12,
  "intro": "Design an <b>informative</b> sign for your school or neighborhood and explain the safe behavior it teaches. See Worked Example 4.",
  "prompts": [{"q": "1. The message of my sign:", "rows": 2}, {"q": "2. Its category, shape, colors and symbol:", "rows": 3}, {"q": "3. The safe behavior it teaches and who needs it:", "rows": 3}]},
 {"id": "act-checklist", "type": "open", "title": "Cyclist Safety Checklist", "rtitle": "Cyclist and signs checklist", "min": 12,
  "intro": "Write a checklist of <b>five safe habits</b> for cyclists (or for walking and riding near bicycles) and one sign you will watch for this week.",
  "prompts": [{"q": "1. Five safe cycling habits:", "rows": 5}, {"q": "2. A sign near your home or school (category and meaning):", "rows": 3}]},
] + exit_acts(["1. Name the three types of vertical signs and describe the shape and color of each.", "2. Write two rules for cyclists and explain why they matter."],
              "Write about five lines. Where do you see traffic signs on your way to school? What do they tell you, and how can you help others follow them?")

W = dict(
  slug="gv8-q2-week-5-road-safety-cyclists-signs", week=5, short="Road Safety: Cyclists and Signs",
  desc="Interactive study page for Growing in Values (8th grade, Q02 Week 5): traffic signs (preventive, regulatory, informative), cyclist safety rules, the helmet and the BRET, with practice.",
  eyebrow="Road education · Cyclists and signs", title="Cyclists and Traffic Signs",
  guiding="“What do traffic signs tell us, and how can a cyclist stay safe and visible?”",
  target="I can classify vertical traffic signs by shape and color, explain the rules for riding a bicycle, and design a sign that teaches a safe behavior.",
  indicator="Shows respect for the road education rules as a pedestrian, cyclist and passenger in the places where they travel.",
  book="pp. 124–127", plan="Road safety: cyclists and signs (S1_U2_C05)",
  learn=learn, ideas=ideas, vocab=vocab, examples=examples, acts=acts,
  method='<div class="card soft"><b>Reading any sign:</b> (1) What is its shape? (2) What are its colors? (3) Which type is it: preventive, regulatory or informative? (4) What should I do?</div>',
  selfcheck=["I can tell preventive, regulatory and informative signs apart.", "I can list four rules for cyclists.", "I can explain what the BRET do.", "I completed my sign design and my exit ticket."],
  motto="Signs and helmets save lives.")
