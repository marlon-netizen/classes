from lib import *

GENS = r'''
window.GV_GENS = { util: function(rnd, k){
  const ri = (a,b) => a + Math.floor(rnd()*(b-a+1));
  if(k===0){ const L = ri(2,6); return {q:'A dripping tap wastes <b>'+L+' liters every hour</b>. How many liters does it waste in <b>24 hours</b>?', ans:L*24, unit:'liters', tol:0.01, hint:'Multiply the liters per hour by 24 hours.', e:L+' liters × 24 hours = '+(L*24)+' liters.'}; }
  if(k===1){ const L = ri(3,7)*10; return {q:'A leaking toilet wastes <b>'+L+' liters every day</b>. How many liters does it waste in <b>one week</b> (7 days)?', ans:L*7, unit:'liters', tol:0.01, hint:'Multiply the liters per day by 7.', e:L+' × 7 = '+(L*7)+' liters.'}; }
  if(k===2){ const N = ri(4,10), W = [10,12,15,18][ri(0,3)], H = ri(4,8), kwh = N*W*H/1000; return {q:'A classroom has <b>'+N+' bulbs</b> of <b>'+W+' watts</b> each, switched on for <b>'+H+' hours</b>. How many <b>kilowatt-hours (kWh)</b> do they use? (kWh = watts × hours ÷ 1000)', ans:kwh, unit:'kWh', tol:0.006, hint:'Total watts = bulbs × watts. Then multiply by hours and divide by 1000.', e:N+' × '+W+' W = '+(N*W)+' W; × '+H+' h = '+(N*W*H)+' Wh; ÷ 1000 = '+kwh+' kWh.'}; }
  if(k===3){ const R = ri(6,9), E = ri(10,30)*10; return {q:'In this simulated example, electricity costs <b>C$ '+R+' per kWh</b> and the school used <b>'+E+' kWh</b> in a month. What is the cost?', ans:R*E, unit:'C$', tol:0.01, hint:'Multiply the price per kWh by the kWh used.', e:R+' × '+E+' = C$ '+(R*E)+'.'}; }
  const A = ri(10,20)*100, P = [10,15,20,25,30][ri(0,4)], B = A*(100-P)/100;
  return {q:'A school used <b>'+A+' liters</b> of water per day. After a saving campaign it used <b>'+B+' liters</b> per day. By what <b>percent</b> did it reduce its use?', ans:P, unit:'%', tol:0.01, hint:'Saved = before − after. Then (saved ÷ before) × 100.', e:'Saved '+(A-B)+' liters; '+(A-B)+' ÷ '+A+' × 100 = '+P+'%.'};
}};
'''

learn = '''
  <div class="card warm">
    <h3>Basic services are shared resources</h3>
    <p><strong>Basic services</strong> are things we need every day: drinking <b>water</b>, <b>electricity</b>, sanitation and waste collection. They come from limited resources and they are paid for by families and by the community (through fees and taxes). <strong>Responsible consumption</strong> means using what we <em>need</em> and avoiding <em>waste</em>.</p>
    <p style="margin:0">The textbook teaches that we love and care for our <b>home, school and community</b>, and that a <b>responsible citizen</b> evaluates the impact of their decisions and uses natural resources rationally.</p>
  </div>
  <div class="card">
    <h3>Where I take care: home, school, community</h3>
    <div class="fact">
      <div><b class="h">Home</b>Tidy my room; pick up clothes and toys; take out the trash; sweep and mop; water the plants.</div>
      <div><b class="h">School</b>Help clean the board; clean desks and furniture; sweep the classroom daily; empty the classroom trash bins; do not scribble on walls; do not slam doors.</div>
      <div><b class="h">Community</b>Sweep gutters and throw out trash along the street; cut weeds in parks; keep public spaces clean.</div>
    </div>
    <p class="ref" style="margin:10px 0 0">The numbers in this week's practice are simulated for learning. Use them to practice, not as real prices.</p>
  </div>
'''

ideas = [
 {"tab": "1. Clean and caring habits", "title": "Habits that protect health and learning", "ref": "Textbook, pp. 66–69",
  "pts": ["A clean, tidy environment protects us from illnesses caused by <b>germs and bacteria</b>, keeps us safe and is essential for good learning.", "<b>Habits</b> are behaviors done daily and permanently; they count as habits only when practiced every day.", "Personal hygiene: wash hands before and after recess, keep nails short and clean, keep hair clean.", "Order prevents accidents: keep floors and aisles free of trash, books and backpacks so no one trips."],
  "key": "Good habits are daily choices, not one-time actions."},
 {"tab": "2. Caring for the classroom", "title": "The classroom is our second home", "ref": "Textbook, pp. 66–69",
  "pts": ["Keeping it in good condition is the responsibility of <b>all students</b>.", "After class, help the teacher clean the board; sweep daily; pick up trash around the school.", "Do not slam the door (it loosens the hinges and can cause accidents) and do not scribble on the walls.", "<b>Respect the class schedule</b>: just as we like our recess respected, we respect teachers' time."],
  "key": "A shared space stays pleasant only when everyone cares for it."},
 {"tab": "3. What are basic services?", "title": "Basic services", "ref": "Responsible consumption",
  "pts": ["<b>Water:</b> for drinking, cooking, hygiene and cleaning.", "<b>Electricity:</b> for light, fans, computers and appliances.", "<b>Sanitation and waste collection:</b> keep homes, schools and streets healthy.", "These services use limited resources and cost money to produce, deliver and maintain."],
  "key": "Every liter and every kilowatt-hour counts."},
 {"tab": "4. Need or waste?", "title": "Need vs. waste", "ref": "Responsible consumption",
  "pts": ["A <b>need</b>: using the water or energy that a task really requires (a short shower, light when it is dark).", "<b>Waste</b>: using more than necessary (a tap running while brushing teeth, lights in an empty room, a leak that nobody fixes).", "Ask: <b>Do I need it now? Is there a way to use less? Can I fix or report a leak?</b>"],
  "key": "Responsible consumption means using what I need and not more."},
 {"tab": "5. A simulated audit", "title": "Auditing consumption (simulation)", "ref": "Class activity",
  "pts": ["1. Choose a place (classroom, bathroom, yard).", "2. List the water and electricity uses there.", "3. Estimate how much each use takes (liters, watts and hours).", "4. Mark which uses are <b>needs</b> and which are <b>waste</b>.", "5. Plan measures (for example turn off lights, report leaks, close taps).", "6. Set a goal and check later."],
  "key": "Measuring first lets us save with purpose."},
 {"tab": "6. Responsible citizen", "title": "The responsible citizen", "ref": "Textbook, p. 114",
  "pts": ["A responsible citizen <b>exercises rights and obligations</b>, such as paying taxes, caring for the environment and respecting other people's rights.", "Responsible citizens <b>evaluate the impact of their decisions</b>, positive or negative, on others.", "We must commit to respecting the environment, making <b>rational use of natural resources</b> and acting against pollution."],
  "key": "My small daily choices have an impact on everyone."},
]

vocab = [
 ["Consumption", "The use of goods and services, like water, light or food."],
 ["Responsible consumption", "Using only what is needed and caring about the effect on others and the environment."],
 ["Waste", "Using or throwing away more than is needed."],
 ["Basic services", "Essential services such as drinking water, electricity, sanitation and waste collection."],
 ["Kilowatt-hour (kWh)", "The unit used to measure electricity consumption."],
 ["Leak", "A small opening that lets water or fluid escape."],
 ["Habit", "A behavior done daily and permanently."],
 ["Impact", "The effect an action has on people or the environment."],
 ["Hygiene", "Practices that keep us clean and healthy (aseo)."],
]

examples = [
 {"title": "Example 1: Need or waste?",
  "problem": "<i>A student leaves the classroom at recess and does not turn off the fan and the lights.</i> Is that a need or waste?",
  "steps": [["Ask: is anyone using them?", "No, the room is empty."],
            ["Ask: do we need them now?", "No."],
            ["Decide.", "Using energy that nobody needs is <b>waste</b>."],
            ["Propose an action.", "Turn off the fan and the lights when the last person leaves, or assign a “light monitor.”"],
            ["Answer.", "It is <b>waste</b>. The solution is to switch them off when leaving the room.", True]]},
 {"title": "Example 2: Calculate a leak",
  "problem": "A dripping tap wastes <b>4 liters per hour</b>. How much water does it waste in a day?",
  "steps": [["Write what you know.", "4 liters per hour."],
            ["Decide the operation.", "One day has 24 hours: multiply."],
            ["Calculate.", "4 × 24 = 96."],
            ["Check the unit.", "Liters."],
            ["Answer.", "The tap wastes <b>96 liters a day</b>. A quick repair saves all of it.", True]]},
 {"title": "Example 3: Electricity in a classroom",
  "problem": "6 bulbs of 15 watts are on for 8 hours. How many kWh do they use?",
  "steps": [["Total watts.", "6 × 15 = 90 W."],
            ["Watt-hours.", "90 W × 8 h = 720 Wh."],
            ["Convert to kWh.", "720 ÷ 1000 = 0.72 kWh."],
            ["Answer.", "They use <b>0.72 kWh</b>. If they are on 2 fewer hours, they use 0.18 kWh less.", True]]},
 {"title": "Example 4: Write a checkable saving commitment",
  "problem": "Write a commitment to save water or electricity that you can check.",
  "steps": [["Vague idea.", "“I will save water.”"],
            ["Problem.", "No one can check it."],
            ["Name the action and amount.", "“I will turn off the tap while brushing my teeth.”"],
            ["Add when and how I will check.", "“Every morning and night for one week; I will mark a calendar each day.”"],
            ["Check it.", "Specific ✓ Possible ✓ Has a time ✓ I can verify it ✓"],
            ["Final commitment.", "<i>For one week I will turn off the tap while brushing my teeth every morning and night. I will mark each day on a calendar.</i>", True]]},
]

quiz = [
 Q("Which of these are basic services?", ["Drinking water, electricity and waste collection", "Video games and movies", "Toys and clothes", "Restaurant meals"], "Basic services are essential for daily life."),
 Q("What does responsible consumption mean?", ["Using what we need and avoiding waste", "Using as much as possible", "Never using water or electricity", "Buying the most expensive item"], "It means using the resources we need without waste."),
 Q("Which action is waste?", ["Leaving a tap running while brushing teeth", "Turning on a light when it is dark", "Taking a short shower", "Washing hands before eating"], "Water that is not being used is lost."),
 Q("Which action saves electricity?", ["Turning off lights and fans in an empty room", "Leaving all lights on", "Leaving the computer on all night", "Opening the fridge often"], "Switching off what is not needed saves energy."),
 Q("Why is a clean, tidy environment important (textbook)?", ["It protects us from germs and bacteria, keeps us safe and helps learning", "It looks fancy", "It is a rule only for teachers", "It is not important"], "A clean place protects health and learning."),
 Q("What is a habit?", ["A behavior done daily and permanently", "A one-time action", "A gift", "A hobby only"], "Habits count only when practiced every day."),
 Q("Who is responsible for keeping the classroom in good condition?", ["All the students", "Only the teacher", "Only the cleaning staff", "Nobody"], "The textbook says it is the responsibility of all students."),
 Q("What does a responsible citizen do?", ["Exercises rights and duties, like caring for the environment and respecting others", "Only demands rights", "Ignores rules", "Wastes resources"], "A responsible citizen evaluates the impact of their decisions."),
 Q("A school finds a leaking tap. What is the best response?", ["Report it so it can be fixed", "Ignore it", "Wait for it to stop", "Turn the sink over"], "Leaks waste a lot of water and can be fixed easily."),
 Q("Why must we respect the class schedule?", ["Every moment has its time, and we expect our recess to be respected too", "It is not important", "Only teachers have schedules", "To avoid homework"], "Respecting time is respecting others."),
]

acts = [
 {"id": "act-quiz", "type": "quiz", "title": "Mastery Quiz (10 questions)", "intro": "Ten questions on responsible consumption and caring for spaces. Aim for 80% or higher.", "qs": quiz},
 {"id": "act-care", "type": "sort", "title": "I Care for My Home, School and Community", "intro": "From your textbook activity: where does each action belong?",
  "choices": [{"k": "H", "label": "🏠 Home"}, {"k": "S", "label": "🏫 School"}, {"k": "C", "label": "🌳 Community"}],
  "cards": [["Tidy my room and pick up clothes and toys.", "H", "That is care for the home."], ["Clean the desks and other furniture in my classroom.", "S", "That is care for the school."], ["Sweep the gutters and throw out the trash along the street.", "C", "That is care for the community."],
            ["Take out the trash at my house.", "H", "That is care for the home."], ["Empty the trash bins in my classroom.", "S", "That is care for the school."], ["Cut the weeds in the park.", "C", "That is care for the community."], ["Help the teacher clean the board.", "S", "That is care for the school."], ["Sweep and mop the floors at home.", "H", "That is care for the home."]]},
 {"id": "act-need", "type": "sort", "title": "Need or Waste?", "intro": "Decide whether each use of water or electricity is a <b>need</b> or <b>waste</b>.",
  "choices": [{"k": "N", "label": "✅ Need"}, {"k": "W", "label": "🚫 Waste"}],
  "cards": [["Leaving the tap running while you brush your teeth.", "W", "Close the tap when you are not using the water."], ["Switching on the lights in a dark classroom.", "N", "You need light to see."], ["Leaving the lights and fans on in an empty classroom.", "W", "Nobody is using them."],
            ["Using the water you need to wash your hands before eating.", "N", "Hygiene is a need."], ["Ignoring a tap that leaks all day.", "W", "A leak wastes liters every hour."], ["Opening the curtains and using natural light on a sunny morning.", "N", "Using daylight is smart use, not waste."],
            ["Leaving a computer on all night.", "W", "Switch it off when you are not using it."], ["Filling a bucket only as much as you need to mop.", "N", "You used what the task required."]]},
 {"id": "act-calc", "type": "calc", "gen": "util", "n": 5, "title": "Audit Numbers (your own set)", "rtitle": "Audit numbers (practice with simulated data)",
  "intro": "Practice for the school audit. Each classmate gets a different set of numbers. The numbers are simulated."},
 {"id": "act-match", "type": "match", "title": "Match the Saving Habit", "intro": "Tap the situation, then the best saving habit.",
  "pairs": [["Dripping tap", "Report and fix the leak"], ["Brushing teeth", "Close the tap while brushing"], ["Empty classroom", "Turn off lights and fans"], ["Sunny morning", "Use natural light"], ["Computer not in use", "Switch it off"], ["Trash on the street", "Sweep and put it in the bin"], ["Dirty classroom board", "Help the teacher clean it"]]},
 {"id": "act-seq", "type": "seq", "title": "Steps of a School Audit (simulation)", "intro": "Put the steps of a simulated consumption audit in order.",
  "items": [{"t": "Choose a place to audit (for example the classroom)", "hint": "Start by deciding where to look.", "why": "A focused place is easier to measure."},
            {"t": "List the water and electricity uses there", "hint": "Write down what is used.", "why": "First list the uses."},
            {"t": "Estimate how much each use consumes", "hint": "Use liters or watts × hours.", "why": "Estimate liters, watts and hours."},
            {"t": "Separate needs from waste", "hint": "Compare each use with what is needed.", "why": "Identify the waste."},
            {"t": "Plan saving measures and set a goal", "hint": "What will you change?", "why": "Measures + goal give direction."},
            {"t": "Check later whether consumption went down", "hint": "The final step.", "why": "Checking shows if the measures work."}]},
 {"id": "act-multi", "type": "multi", "title": "Select All That Apply", "intro": "Some questions have more than one right answer.",
  "qs": [{"q": "Which actions save water?", "o": ["Fix leaks", "Close the tap while brushing teeth", "Take shorter showers", "Leave a hose running"], "a": [0, 1, 2], "e": "A running hose wastes water."},
         {"q": "Which actions save electricity?", "o": ["Turn off lights when leaving", "Use natural light in the day", "Switch off unused devices", "Leave fans on in an empty room"], "a": [0, 1, 2], "e": "An empty room does not need a fan."},
         {"q": "Which show care for the school (textbook)?", "o": ["Not scribbling on walls", "Not slamming the door", "Picking up trash", "Leaving backpacks in the aisle"], "a": [0, 1, 2], "e": "Backpacks in the aisle can make someone trip."},
         {"q": "Which are good personal hygiene habits?", "o": ["Washing hands before and after recess", "Keeping nails short and clean", "Keeping hair clean", "Spitting on the floor"], "a": [0, 1, 2], "e": "Spitting on the floor is unhygienic."}]},
 {"id": "act-cloze", "type": "cloze", "title": "Complete the Sentences", "intro": "Choose the word that completes each sentence.",
  "items": [["A ", ["habit", "holiday", "gift"], 0, " is a behavior done daily and permanently.", "Habits are practiced every day."],
            ["Using more water than needed is ", ["waste", "a need", "a habit"], 0, ".", "Waste is using more than required."],
            ["Electricity is measured in ", ["kilowatt-hours", "liters", "meters"], 0, ".", "kWh."],
            ["A ", ["leak", "plant", "poster"], 0, " can waste many liters of water.", "A leak wastes water every hour."],
            ["The classroom is our ", ["second", "last", "first"], 0, " home.", "It is the place where we spend most of our time."],
            ["A responsible citizen evaluates the ", ["impact", "price", "color"], 0, " of their decisions.", "Our choices affect others."]]},
 {"id": "act-scen", "type": "scenario", "title": "What Would You Do?", "intro": "Choose the best response in each situation.",
  "steps": [{"s": "You see a tap dripping in the school bathroom. What do you do?", "o": [
              {"t": "Close it tightly and tell a teacher or the maintenance staff so the leak can be repaired.", "p": 2, "f": "You act and make sure it gets fixed."},
              {"t": "Close it but tell nobody.", "p": 1, "f": "Good start; a leak needs repair."},
              {"t": "Ignore it; it is not your tap.", "p": 0, "f": "School resources belong to everyone."}]},
            {"s": "At lunch, a friend leaves the water running while washing their hands for a long time. What is a good response?", "o": [
              {"t": "Kindly remind them to close the tap while they soap their hands, and explain how many liters are wasted.", "p": 2, "f": "Kind, specific and educational."},
              {"t": "Laugh at them.", "p": 0, "f": "Mocking does not teach."},
              {"t": "Wait for them to finish silently.", "p": 1, "f": "You did not help change the habit."}]},
            {"s": "Your family's electricity bill is high. What can you do?", "o": [
              {"t": "Look for waste at home (lights, devices, fans), make a plan with your family, and check the bill next month.", "p": 2, "f": "Audit, plan and check."},
              {"t": "Tell your family to buy a different bulb.", "p": 1, "f": "One change helps a little but habits matter more."},
              {"t": "Do nothing; bills always go up.", "p": 0, "f": "Our choices can change the bill."}]},
            {"s": "On the way out of the classroom you see trash on the floor that is not yours. What do you do?", "o": [
              {"t": "Pick it up and put it in the bin. The classroom is everyone's responsibility.", "p": 2, "f": "You care for a shared space."},
              {"t": "Leave it for the cleaning staff.", "p": 0, "f": "The textbook says all students are responsible."},
              {"t": "Tell someone else to pick it up.", "p": 1, "f": "Better to act yourself."}]}]},
 {"id": "act-audit", "type": "open", "title": "My School Audit", "rtitle": "Simulated consumption audit", "min": 15,
  "intro": "Choose one place at school (classroom, bathroom, yard) and complete a simulated audit. See the steps in the sequence activity.",
  "prompts": [{"q": "1. The place I audit and its uses of water or electricity:", "rows": 3}, {"q": "2. Which uses are needs and which are waste? Explain.", "rows": 4}, {"q": "3. Two saving measures and a goal:", "rows": 3}]},
 {"id": "act-commit", "type": "open", "title": "My Saving Commitment", "rtitle": "Saving commitment for a basic service", "min": 15,
  "intro": "Create a commitment to save one basic service that you can <b>check</b>. See Worked Example 4.",
  "prompts": [{"q": "1. Which service and what will I do?", "rows": 3}, {"q": "2. For how long and how will I check that I did it?", "rows": 3}]},
 {"id": "act-book", "type": "open", "title": "Book Review Questions", "rtitle": "Review questions (Creciendo en Valores, p. 69)", "min": 20,
  "intro": "From your textbook (Tema 11).",
  "prompts": [{"q": "1. Why is a clean, tidy environment important?", "rows": 3}, {"q": "2. Explain how good hygiene is achieved.", "rows": 3}, {"q": "3. What should be done to strengthen personal hygiene habits?", "rows": 3}, {"q": "4. Why should scribbling on walls be avoided?", "rows": 2}, {"q": "5. Why must we respect the class schedule?", "rows": 2}]},
] + exit_acts(["1. Explain the difference between a need and waste, with one example at school.", "2. What is your saving commitment and how will you check it?"],
              "Write about five lines. What did you notice at home or at school about water, electricity or cleanliness, and what will you change?")

W = dict(
  slug="gv8-q2-week-6-responsible-use-of-basic-services", week=6, short="Responsible Use of Basic Services",
  desc="Interactive study page for Growing in Values (8th grade, Q02 Week 6): responsible consumption of water and electricity, caring for home, school and community, a simulated audit and savings commitment.",
  eyebrow="Responsible consumption · Basic services", title="Using Basic Services Responsibly",
  guiding="“How can my family, my school and I use water and electricity without waste?”",
  target="I can tell needs from waste, calculate simple consumption and savings, carry out a simulated audit at school, and make a saving commitment I can check.",
  indicator="Shows habits of responsible consumption in the use of basic services in the family, the school and the community.",
  book="pp. 66–70 and 113–114", plan="Responsible consumption of basic services (S1_U2_C06)",
  learn=learn, ideas=ideas, vocab=vocab, examples=examples, acts=acts, gens=GENS,
  method='<div class="card soft"><b>The four audit questions:</b> (1) What is used? (2) How much? (3) Is it a need or waste? (4) What measure will I take?</div>',
  selfcheck=["I can tell a need from waste with examples.", "I can calculate a leak or an electricity use.", "I can name three ways to care for my home, school and community.", "I wrote my saving commitment and my exit ticket."],
  motto="Every liter and every kilowatt-hour counts.")
