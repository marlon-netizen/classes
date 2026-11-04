from lib import *

learn = '''
  <div class="card warm">
    <h3>I take care of my life and the lives of others</h3>
    <p>Safe traffic depends on <strong>what each of us does</strong>. Every day we travel in three roles: as a <b>pedestrian</b> (on foot), as a <b>passenger</b> and, one day, as a <b>driver</b>. Each role has rules that protect lives.</p>
    <p style="margin:0"><em>“Be careful, preserve your life and that of others. Before crossing the street, make sure to look both ways.”</em> (textbook, p. 117)</p>
  </div>
  <div class="card">
    <h3>Three roles, three sets of responsibilities</h3>
    <div class="fact">
      <div><b class="h">Pedestrian</b>Everyone who travels on foot is a pedestrian, including people who push a bicycle or a motorcycle with the engine off and people who move in a wheelchair. Pedestrians must take precautions and respect the rules for crossing.</div>
      <div><b class="h">Passenger</b>Wait for transport in safe places (the sidewalk, not the roadway), do not get on or off a moving bus, wear the seat belt, and do not distract the driver.</div>
      <div><b class="h">Driver</b>Drives at moderate speed, takes no risks, never drives after drinking, respects signals and the rights of others, and avoids distractions such as the phone.</div>
    </div>
    <div class="fig" style="margin-top:12px">%s%s%s</div>
    <p class="ref" style="margin:6px 0 0">The traffic light: red = stop, yellow = caution, green = go (when it is clear).</p>
  </div>
''' % (traffic_light("r"), traffic_light("y"), traffic_light("g"))

ideas = [
 {"tab": "1. Pedestrian", "title": "The pedestrian: who is it?", "ref": "Textbook, p. 117",
  "pts": ["Every person who travels <b>on foot</b> on traffic routes is a pedestrian. This includes people who <b>push a bicycle or a motorcycle with the engine off</b> and people who move in a <b>wheelchair</b>.", "Pedestrians must <b>take precautions</b> and respect the specific rules.", "Before crossing, <b>look both ways</b> along the road."],
  "key": "Pedestrians are protected best when they are careful and visible."},
 {"tab": "2. Crossing safely", "title": "Crossing the street with caution", "ref": "Textbook, p. 121",
  "pts": ["Memorize the three steps: <b>1.</b> Look first to the <b>left</b>. <b>2.</b> Then to the <b>right</b>. <b>3.</b> Before you start to cross, look again to the <b>left</b>.", "Always use the <b>pedestrian crossings</b>.", "If the crossing has a traffic light, <b>do not cross on red or flashing light</b>: wait on the sidewalk until it is green, and still check that no vehicle is coming.", "Be careful near garages and workshops: vehicles may come out."],
  "key": "Look left, look right, look left again, and cross at the crossing."},
 {"tab": "3. A good pedestrian", "title": "What a good pedestrian does", "ref": "Textbook, pp. 121–122",
  "pts": ["Always walk on the <b>sidewalks</b>; if you play, do not bother or block others.", "Always use the pedestrian crossings.", "Respect traffic lights: wait for green.", "Be careful when you pass beside a garage or workshop.", "<b>Give way to older people</b> when the sidewalks are narrow."],
  "key": "A good pedestrian is careful and considerate."},
 {"tab": "4. Passenger", "title": "The passenger's rules", "ref": "Textbook, pp. 117–118",
  "pts": ["Wait for transport in safe areas, <b>on the sidewalk, not on the roadway</b>.", "<b>Do not get on or off</b> while the vehicle is moving.", "<b>Always wear the seat belt</b>, including in the back seat.", "<b>Do not distract the driver;</b> it can cause accidents.", "Warn the driver if you see unsafe conditions, give directions in time and, on a long trip, help the driver stay alert by talking to them.", "Call the driver's attention if they are driving dangerously."],
  "key": "A passenger is part of the safety of the trip."},
 {"tab": "5. Driver", "title": "A good driver", "ref": "Textbook, pp. 118–121",
  "pts": ["A good driver <b>drives at moderate speed, makes no risky maneuvers, does not drink alcohol when driving</b>, drives responsibly and respects traffic rules and the rights of others.", "Respect <b>traffic lights and signs</b>: running a red light or ignoring a STOP is very dangerous.", "Do not park on avenues or roundabouts and do not block intersections.", "Use <b>turn signals</b>; keep the car in good condition; travel on the right; avoid distractions such as the phone; use warning triangles after a breakdown."],
  "key": "Responsible driving protects every person on the road."},
 {"tab": "6. Why rules matter", "title": "Why do we follow the rules?", "ref": "Values",
  "pts": ["Rules protect <b>life</b>, mine and other people's.", "Following them is a sign of <b>respect and responsibility</b>.", "Even when nobody is watching, we choose the safe behavior.", "We can also <b>teach others</b>: reminding a friend to buckle up is an act of care."],
  "key": "Road safety is a value: care for life."},
]

vocab = [
 ["Precaution", "Care taken to avoid a danger."],
 ["Roadway", "The part of the road where vehicles travel (calzada)."],
 ["Frustration", "The feeling of anger or sadness when things do not go as we want."],
 ["Visibility", "How well something can be seen."],
 ["Traffic flow", "The smooth movement of vehicles (fluidez)."],
 ["Flashing light", "A light that blinks on and off (intermitente)."],
 ["Pedestrian", "A person who travels on foot."],
 ["Passenger", "A person who travels in a vehicle but does not drive it."],
 ["Seat belt", "A strap that holds a person in the seat if the vehicle stops suddenly."],
]

examples = [
 {"title": "Example 1: Crossing at a corner",
  "problem": "You want to cross a street at a corner that has a pedestrian crossing and a traffic light. What do you do?",
  "steps": [["Stand on the sidewalk.", "Wait at the curb, where drivers can see you."],
            ["Read the light.", "Do not cross on red or flashing light. Wait for green."],
            ["Look left, right, and left again.", "Check that no vehicle is coming, even when the light is green for you."],
            ["Cross at the crossing.", "Walk steadily and keep your attention on the road."],
            ["Answer.", "Wait for green, look left, right and left again, then cross at the crossing.", True]]},
 {"title": "Example 2: Getting on the bus",
  "problem": "<i>A bus is leaving the stop. A student runs, steps off the sidewalk and tries to jump on while it moves.</i>",
  "steps": [["Which rule applies?", "Passengers wait on the sidewalk and <b>do not get on or off a moving vehicle</b>."],
            ["What could happen?", "A fall under the wheels or a collision with other vehicles."],
            ["What is the safe choice?", "Wait for the next bus on the sidewalk."],
            ["Answer.", "Let the bus go. Wait safely on the sidewalk for the next one.", True]]},
 {"title": "Example 3: Passenger and driver",
  "problem": "<i>You are in the front seat. The driver keeps looking at the phone and drives fast.</i>",
  "steps": [["Name the risk.", "Distraction and speed."],
            ["Recall the passenger's duties.", "Warn the driver of unsafe conditions and call attention if the driving is dangerous."],
            ["Choose the words.", "Calm and clear: “Please put the phone away and slow down. I want us all to arrive safely.”"],
            ["Protect yourself too.", "Wear your seat belt and, if the driver does not change, ask to get out safely and tell an adult."],
            ["Answer.", "Speak up calmly, keep your belt fastened and ask for safer driving. Do not distract the driver with arguments.", True]]},
 {"title": "Example 4: Design a safe route",
  "problem": "Plan the safest route from your house to your school as a pedestrian.",
  "steps": [["Draw the route.", "Mark start (home) and end (school)."],
            ["Mark the crossings.", "Choose streets that have <b>pedestrian crossings</b> and traffic lights."],
            ["List risk points.", "Garages, narrow sidewalks, busy corners."],
            ["Write the safe action for each.", "Look left-right-left, give way on narrow sidewalks, wait for green."],
            ["Final route.", "<table class='cmp'><tr><th>Place</th><th>Safe action</th></tr><tr><td>Main avenue crossing</td><td>Wait for green; look left, right, left</td></tr><tr><td>Garage entrance</td><td>Slow down and watch for vehicles</td></tr><tr><td>Narrow sidewalk</td><td>Give way to older people</td></tr></table>", True]]},
]

quiz = [
 Q("Who is a pedestrian?", ["Anyone who travels on foot, including a person pushing a bicycle with the engine off or using a wheelchair", "Only people walking fast", "Only adults", "Drivers of small cars"], "The textbook includes people who push a bicycle or a motorcycle with the engine off and people with disabilities in wheelchairs."),
 Q("What is the first thing to do before crossing a street?", ["Look both ways along the road", "Run", "Close your eyes", "Call a friend"], "Looking both ways is the first precaution."),
 Q("The three steps for crossing are…", ["Look left, look right, look left again", "Look right only", "Run and look later", "Look at the phone, then cross"], "Left, right, and left again just before you start."),
 Q("A pedestrian crossing has a red or flashing light. What do you do?", ["Wait on the sidewalk until it is green", "Cross quickly", "Cross if the street looks empty", "Run across"], "Do not cross on red or flashing."),
 Q("Where should passengers wait for transport?", ["On the sidewalk, in a safe area", "On the roadway", "Between parked cars", "In the middle of the street"], "Safe areas are sidewalks and designated stops."),
 Q("A passenger should…", ["Always wear the seat belt, including in the back seat", "Wear the belt only in front", "Not wear it on short trips", "Take it off when the driver is not watching"], "Everyone buckles up, every time."),
 Q("Why should a passenger not distract the driver?", ["It can cause accidents", "It makes the trip shorter", "Drivers like noise", "It is rude only"], "A distracted driver can crash."),
 Q("Which describes a good driver?", ["Moderate speed, no risky maneuvers, no alcohol, respects traffic rules", "The fastest driver", "One who ignores signs at night", "One who talks on the phone"], "A good driver is careful and responsible."),
 Q("Why is it dangerous to ignore a STOP sign or a red light?", ["Because it can cause serious collisions, especially at night", "It is only impolite", "It saves time and is safe", "It is dangerous only for pedestrians"], "Ignoring signals puts everyone at risk."),
 Q("On narrow sidewalks, a good pedestrian…", ["Gives way to older people", "Walks in the middle", "Runs ahead", "Blocks the way"], "A good pedestrian is considerate."),
]

acts = [
 {"id": "act-quiz", "type": "quiz", "title": "Mastery Quiz (10 questions)", "intro": "Ten questions on pedestrian, passenger and driver responsibilities. Aim for 80% or higher.", "qs": quiz},
 {"id": "act-lights", "type": "quiz", "title": "Read the Traffic Light", "intro": "Look at each traffic light (simplified drawings).",
  "qs": [Q("What does a pedestrian do when the light for the crossing shows this?", ["Wait on the sidewalk and do not cross", "Cross quickly", "Cross if there are no cars", "Run across"], "Red means stop and wait.", traffic_light("r")),
         Q("The light turns yellow as you are about to step off the curb. What do you do?", ["Wait for the next green; yellow is a warning that the light is changing", "Hurry across", "Walk slowly across", "Ignore it"], "Yellow is a caution: do not start to cross.", traffic_light("y")),
         Q("The light is green for pedestrians. What do you still do before stepping out?", ["Look left, right and left again to check that no vehicle is coming", "Nothing, green is always safe", "Close your eyes", "Run"], "Green means you may go if it is clear: always check.", traffic_light("g")),
         Q("A driver sees this light. What should the driver do?", ["Stop", "Speed up", "Honk and go", "Slow down only"], "Red means stop for drivers too.", traffic_light("r"))]},
 {"id": "act-roles", "type": "sort", "title": "Pedestrian, Passenger or Driver?", "intro": "Who does each safe behavior belong to most?",
  "choices": [{"k": "P", "label": "🚶 Pedestrian"}, {"k": "S", "label": "🚌 Passenger"}, {"k": "D", "label": "🚗 Driver"}],
  "cards": [["Look left, right and left again before crossing.", "P", "Pedestrians look in all directions before they cross."], ["Wait for the green light on the sidewalk.", "P", "Pedestrians obey the light."],
            ["Do not get on or off while the bus is moving.", "S", "Passengers wait until the vehicle stops."], ["Wear the seat belt, even in the back seat.", "S", "Passengers always use the belt."], ["Warn the driver about unsafe conditions.", "S", "A passenger helps the driver stay alert."],
            ["Use turn signals before changing lanes.", "D", "Signals help others react in time."], ["Never drive after drinking alcohol.", "D", "A good driver does not drink alcohol when driving."], ["Keep the vehicle in good mechanical condition.", "D", "A defective car is dangerous."], ["Give way to older people on narrow sidewalks.", "P", "A good pedestrian is considerate."]]},
 {"id": "act-risk", "type": "sort", "title": "Safe or Risky?", "intro": "Is each situation <b>safe</b> or <b>risky</b>?",
  "choices": [{"k": "S", "label": "🟢 Safe"}, {"k": "R", "label": "🔴 Risky"}],
  "cards": [["Crossing at the crossing after the light turns green and looking left, right, left.", "S", "That is the correct way to cross."], ["Crossing the street while looking at a phone.", "R", "You cannot see danger when you are distracted."], ["Standing on the roadway to wait for the bus.", "R", "Wait on the sidewalk."],
            ["Wearing the seat belt in the back seat.", "S", "Seat belts are for everyone."], ["Running to jump on a moving bus.", "R", "Never get on or off a moving vehicle."], ["Asking the driver kindly to slow down.", "S", "A passenger can help the driver be safe."],
            ["Crossing on a flashing light because the street looks empty.", "R", "Do not cross on red or flashing lights."], ["Walking past a garage and checking for vehicles coming out.", "S", "Vehicles may come out of garages."]]},
 {"id": "act-match", "type": "match", "title": "Match the Rule", "intro": "Tap the situation on the left, then the right behavior.",
  "pairs": [["Crossing a street", "Look left, right and left again"], ["Waiting for a bus", "Stay on the sidewalk"], ["Inside a vehicle", "Wear the seat belt, front and back"], ["Traffic light is red or flashing", "Wait; do not cross"], ["Narrow sidewalk", "Give way to older people"], ["Long trip with a tired driver", "Talk to the driver to keep them alert"], ["Driver breaks down", "Place warning triangles"]]},
 {"id": "act-seq", "type": "seq", "title": "Crossing the Street Safely", "intro": "Put the steps in order.",
  "items": [{"t": "Stop at the curb and find the pedestrian crossing", "hint": "Find the safest place first.", "why": "Use the pedestrian crossing."},
            {"t": "Wait for the green light on the sidewalk", "hint": "Be patient before stepping out.", "why": "Do not cross on red or flashing."},
            {"t": "Look to the left", "hint": "The first of the three looks.", "why": "First look: left."},
            {"t": "Look to the right", "hint": "The second look.", "why": "Second look: right."},
            {"t": "Look again to the left before you start to cross", "hint": "The third and final look.", "why": "Third look: left again."},
            {"t": "Cross at a steady walk, eyes up and phone away", "hint": "Now you can move.", "why": "Walk steadily, without distractions."}]},
 {"id": "act-multi", "type": "multi", "title": "Select All That Apply", "intro": "Some questions have more than one right answer.",
  "qs": [{"q": "Which are good passenger behaviors?", "o": ["Wear the seat belt in the back seat", "Wait on the sidewalk", "Warn the driver of danger", "Get off while the bus is moving"], "a": [0, 1, 2], "e": "Never get off a moving vehicle."},
         {"q": "Which are good pedestrian behaviors?", "o": ["Use the pedestrian crossing", "Wait for the green light", "Walk on the sidewalk", "Cross on a flashing light"], "a": [0, 1, 2], "e": "Do not cross on red or flashing lights."},
         {"q": "Which describe a good driver?", "o": ["Moderate speed", "Respects traffic rules", "Does not drink alcohol when driving", "Takes risky maneuvers"], "a": [0, 1, 2], "e": "Risky maneuvers cause accidents."},
         {"q": "Which can distract a driver?", "o": ["A cell phone", "Changing a radio station", "Loud arguments", "Keeping both hands on the wheel"], "a": [0, 1, 2], "e": "Keeping both hands on the wheel helps."}]},
 {"id": "act-cloze", "type": "cloze", "title": "Complete the Sentences", "intro": "Choose the word that completes each sentence.",
  "items": [["Before crossing, look left, right and ", ["left", "up", "behind"], 0, " again.", "Three looks: left, right, left."],
            ["Passengers wait on the ", ["sidewalk", "roadway", "bridge"], 0, ".", "Safe areas, not the roadway."],
            ["Always wear the seat ", ["belt", "cap", "lock"], 0, ", also in the back seat.", "Everyone buckles up."],
            ["Do not cross on a red or ", ["flashing", "green", "blue"], 0, " light.", "Wait for green."],
            ["A good driver does not drink ", ["alcohol", "water", "tea"], 0, " when driving.", "Alcohol and driving never go together."],
            ["Road safety is the responsibility of ", ["everyone", "no one", "police only"], 0, ".", "Safe traffic depends on what each of us does."]]},
 {"id": "act-scen", "type": "scenario", "title": "What Would You Do?", "intro": "Choose the best response in each situation.",
  "steps": [{"s": "Your friends decide to cross in the middle of the block, away from the crossing, to save time. What do you do?", "o": [
              {"t": "Walk to the crossing and invite them to come, explaining it is safer.", "p": 2, "f": "You choose the safe option and offer leadership."},
              {"t": "Follow them quietly.", "p": 0, "f": "Following puts you at risk."},
              {"t": "Cross after them once the street is clear.", "p": 0, "f": "A clear street can change in a second."}]},
            {"s": "The bus is crowded and a student hangs from the door as it moves. What is the best action for you as a passenger?", "o": [
              {"t": "Wait for the next bus rather than hang from the door, and tell the driver or an adult about the dangerous behavior.", "p": 2, "f": "You protect yourself and others."},
              {"t": "Hang from the door too, only for a short ride.", "p": 0, "f": "Short rides are not safer."},
              {"t": "Say nothing but stay inside.", "p": 1, "f": "Staying inside is safe, but you could also warn the driver."}]},
            {"s": "Your older cousin is driving and starts texting. What do you do?", "o": [
              {"t": "Ask calmly that they put the phone away or stop in a safe place to answer, and keep your seat belt on.", "p": 2, "f": "You speak up kindly and stay safe."},
              {"t": "Offer to read the message aloud.", "p": 1, "f": "Offering to help is kind, but the driver is still distracted."},
              {"t": "Pretend not to notice.", "p": 0, "f": "Passengers should warn the driver of danger."}]},
            {"s": "On a narrow sidewalk an older adult with a cane is walking toward you. What is a good pedestrian to do?", "o": [
              {"t": "Step aside and give way.", "p": 2, "f": "Giving way to older people shows respect."},
              {"t": "Keep walking at the same speed.", "p": 0, "f": "That blocks the way."},
              {"t": "Wait until the person passes but keep playing on your phone.", "p": 1, "f": "Waiting is good; paying attention is better."}]}]},
 {"id": "act-route", "type": "open", "title": "My Safe Route and Pledge", "rtitle": "Safe route and pledge", "min": 15,
  "intro": "Design the safest route you use as a pedestrian or passenger (for example home to school). See Worked Example 4.",
  "prompts": [{"q": "1. My route (from … to …) and the crossings I use:", "rows": 3}, {"q": "2. Two risk points on my route and the safe action for each:", "rows": 4}, {"q": "3. My road-safety pledge for this week (concrete and realistic):", "rows": 3}]},
 {"id": "act-mural", "type": "open", "title": "Mural Newspaper: Preventing Accidents", "rtitle": "Mural newspaper: how to prevent traffic accidents", "min": 15,
  "intro": "From your textbook: with your team you write a mural newspaper about what can be done to prevent traffic accidents. Write your part here.",
  "prompts": [{"q": "1. A headline for your mural:", "rows": 2}, {"q": "2. Three tips for pedestrians, passengers or drivers:", "rows": 4}, {"q": "3. Your conclusion about what a good pedestrian and a good passenger do:", "rows": 4}]},
 {"id": "act-book", "type": "open", "title": "Book Review Questions", "rtitle": "Review questions (Creciendo en Valores, p. 123)", "min": 20,
  "intro": "From your textbook.",
  "prompts": [{"q": "1. How do you define a driver?", "rows": 3}, {"q": "2. Why is it necessary to respect traffic lights and traffic signs?", "rows": 3}, {"q": "3. Why must we travel on the right?", "rows": 3}, {"q": "4. What does it mean to travel with caution?", "rows": 3}]},
] + exit_acts(["1. Explain the three steps for crossing a street and one rule for passengers.", "2. Which safe habit will you practice this week, and how will you remember it?"],
              "Write about five lines. Describe one safe or unsafe behavior you saw this week on your way to school and what you would change.")

W = dict(
  slug="gv8-q2-week-4-road-safety-pedestrians-passengers", week=4, short="Road Safety: Pedestrians and Passengers",
  desc="Interactive study page for Growing in Values (8th grade, Q02 Week 4): road safety for pedestrians, passengers and drivers, crossing safely and designing a safe route, with practice.",
  eyebrow="Road education · Pedestrians and passengers", title="I Take Care of My Life: Pedestrians and Passengers",
  guiding="“How do my choices as a pedestrian and as a passenger protect me and the people around me?”",
  target="I can explain the safe behaviors of pedestrians, passengers and drivers, cross a street using the three-look rule, and design a safe route with actions for each risk point.",
  indicator="Shows respect for the road education rules as a pedestrian, cyclist and passenger in the places where they travel.",
  book="pp. 117–123", plan="Road safety: pedestrians and passengers (S1_U2_C04)",
  learn=learn, ideas=ideas, vocab=vocab, examples=examples, acts=acts,
  method='<div class="card soft"><b>The four case questions:</b> (1) Who is involved: pedestrian, passenger or driver? (2) Which rule applies? (3) What could happen? (4) What is the safe alternative?</div>',
  selfcheck=["I can explain the three looks before crossing.", "I can name three rules for passengers.", "I can describe what a good driver does.", "I completed my safe route and my exit ticket."],
  motto="Safe roads begin with my choices.")
