from lib import *

GENS = r'''
window.GV_GENS = { tax: function(rnd, k){
  const ri = (a,b) => a + Math.floor(rnd()*(b-a+1));
  if(k===0){ const P = ri(5,25)*20, R = [5,10,15][ri(0,2)]; return {q:'A simulated tax of <b>'+R+'%</b> is added to a purchase of <b>C$ '+P+'</b>. How much is the tax?', ans:P*R/100, unit:'C$', tol:0.01, hint:'Tax = price × rate ÷ 100.', e:P+' × '+R+' ÷ 100 = C$ '+(P*R/100)+'.'}; }
  if(k===1){ const P = ri(5,25)*20, R = [5,10,15][ri(0,2)]; return {q:'A purchase costs <b>C$ '+P+'</b> before a simulated tax of <b>'+R+'%</b>. What is the <b>total</b> you pay?', ans:P+P*R/100, unit:'C$', tol:0.01, hint:'Find the tax first, then add it to the price.', e:'Tax = '+(P*R/100)+'; total = '+P+' + '+(P*R/100)+' = C$ '+(P+P*R/100)+'.'}; }
  if(k===2){ const N = ri(20,60), T = [10,15,20,25][ri(0,3)]; return {q:'In a simulated community fund, <b>'+N+' families</b> each contribute <b>C$ '+T+'</b>. How much is collected?', ans:N*T, unit:'C$', tol:0.01, hint:'Multiply the number of families by the contribution.', e:N+' × '+T+' = C$ '+(N*T)+'.'}; }
  if(k===3){ const B = ri(5,20)*200, p = [10,15,20,25,30,35][ri(0,5)], H = B*p/100; return {q:'A simulated community budget is <b>C$ '+B+'</b>. <b>C$ '+H+'</b> goes to health. What <b>percent</b> of the budget is that?', ans:p, unit:'%', tol:0.01, hint:'Percent = part ÷ whole × 100.', e:H+' ÷ '+B+' × 100 = '+p+'%.'}; }
  const B = ri(10,30)*100, X = ri(2,4)*100, Y = ri(2,5)*100; return {q:'A simulated budget of <b>C$ '+B+'</b> pays for road repairs (<b>C$ '+X+'</b>) and school repairs (<b>C$ '+Y+'</b>). How much is left?', ans:B-X-Y, unit:'C$', tol:0.01, hint:'Subtract both costs from the budget.', e:B+' − '+X+' − '+Y+' = C$ '+(B-X-Y)+'.'};
}};
'''

learn = '''
  <div class="card warm">
    <h3>Taxes build the common good</h3>
    <p><strong>Fiscal education</strong> teaches why taxes exist and what they are for, so that we understand our duty to pay them and to take part as active, responsible citizens. <strong>Taxation</strong> (<i>tributación</i>) is when citizens hand over to the State a certain amount of money so that the State can provide services such as <b>education, health, roads</b> and old-age pensions.</p>
    <p style="margin:0"><em>“The money obtained from the payment of taxes is used for improvements of the country and the well-being of the population.”</em> (textbook, p. 110)</p>
  </div>
  <div class="card">
    <h3>Key terms</h3>
    <div class="fact">
      <div><b class="h">Tribute (tributo)</b>Payments of money that the State demands, in exercise of its power, to obtain resources for its aims. It brings together taxes (<i>impuestos</i>), fees (<i>tasas</i>) and contributions, set by law.</div>
      <div><b class="h">Taxing power (potestad tributaria)</b>The faculty of the State to create, modify or suppress tributes. It is exercised by the Legislative Power and set by law.</div>
      <div><b class="h">Budget (presupuesto)</b>A yearly plan of expected income and planned expenses and investments. It is the basis for transparency in the use of public resources.</div>
    </div>
  </div>
'''

ideas = [
 {"tab": "1. Fiscal education", "title": "Why do we learn about taxes?", "ref": "Textbook, p. 109",
  "pts": ["Fiscal education is a teaching and learning process that aims at an <b>active, participatory, supportive citizenry</b> that fulfills its obligations.", "It is a tool to build <b>tax values</b>: explaining why and what for taxes exist.", "It helps students assume, in the future, <b>tax compliance as a democratic responsibility</b>.", "<i>“It is everyone's responsibility to pay taxes on time.”</i>"],
  "key": "Paying taxes is a way of taking part in the community."},
 {"tab": "2. Taxation & tribute", "title": "Taxation and tribute", "ref": "Textbook, p. 109",
  "pts": ["<b>Taxation:</b> the action by which citizens hand over to the State an amount of money so that the State provides services required in education, health and more.", "It aims for every citizen to have <b>a minimum of well-being</b>, with basic goods and services such as sanitation, education and pensions, especially for people with few resources.", "<b>Tribute:</b> monetary payments that the State demands to obtain resources for its aims. It includes taxes, fees and contributions, which must be set in legal norms."],
  "key": "Taxes are shared contributions that pay for services everyone uses."},
 {"tab": "3. Taxing power", "title": "The taxing power (potestad tributaria)", "ref": "Textbook, p. 110",
  "pts": ["The faculty of the State to <b>create, modify or suppress</b> tributes unilaterally.", "The State needs economic resources to exist and to meet needs such as <b>national defense, internal security, education and health</b>.", "<b>Characteristics:</b> it is inherent to the State; it emanates from the supreme norm (the Constitution); it is exercised by the <b>Legislative Power</b>; it allows imposing contributions by law; it underpins the action of the authorities."],
  "key": "Taxes are created by law, not by whim."},
 {"tab": "4. Social values", "title": "Social values behind taxes", "ref": "Textbook, p. 111",
  "pts": ["<b>Social values</b> are the values recognized as part of the behavior expected from people in a community.", "They strengthen human relations: <b>respect, friendship, justice, freedom, love, honesty, tolerance</b>.", "No value acts alone: together they form a <b>chain of values</b> that gives positive results.", "Paying taxes honestly puts <b>honesty, responsibility, solidarity and justice</b> into practice."],
  "key": "Taxes are about values: honesty, solidarity, responsibility."},
 {"tab": "5. The budget", "title": "The national budget and its stages", "ref": "Textbook, p. 114",
  "pts": ["A budget is usually valid for <b>one year</b> and includes the estimate of all <b>income</b> and the detail of <b>expenses and investments</b>.", "It lets the State estimate resources and distribute them among institutions according to priorities.", "It is the basis for <b>transparency</b>: we can know where public money goes and evaluate results.", "<b>Stages:</b> 1. Formulation · 2. Discussion and approval · 3. Execution · 4. Control and evaluation of results."],
  "key": "A budget shows what a community values: where the money goes."},
 {"tab": "6. Responsible citizen", "title": "The responsible citizen", "ref": "Textbook, pp. 113–114",
  "pts": ["<b>Citizenship</b> is equality of rights and duties, the use of freedom and responsibility.", "A responsible citizen <b>pays taxes</b>, cares for the environment, respects others' rights and evaluates the impact of their decisions.", "<b>Education for citizenship</b> helps build free, respectful, participatory and supportive persons who know their rights and assume their duties."],
  "key": "A good citizen contributes to the common good."},
]

vocab = [
 ["Tax (impuesto)", "Money citizens pay to the State to support public services."],
 ["Tribute (tributo)", "A payment demanded by the State by law: taxes, fees and contributions."],
 ["Taxing power", "The State's faculty to create, modify or suppress tributes."],
 ["Contribution", "A payment that helps fund a service or work."],
 ["Jurisdiction", "The area or people where an authority has power."],
 ["Budget", "A plan of expected income and expenses for a period."],
 ["Transparency", "Being open so that people can see how public money is used."],
 ["Democracy", "A system in which citizens take part and elect their representatives."],
 ["Common good", "What benefits everyone in the community."],
]

examples = [
 {"title": "Example 1: Where does tax money go?",
  "problem": "<i>A student asks: “Why should we pay taxes if nothing changes for me?”</i> Give an answer using examples.",
  "steps": [["Recall the purpose.", "Taxes pay for services the State provides: education, health, roads, security."],
            ["Find examples near you.", "School teachers, a health center, streets and street lights."],
            ["Link to the common good.", "These services benefit everyone, including you."],
            ["Add the value.", "Paying honestly is a way of being responsible and supportive."],
            ["Answer.", "Taxes pay for services like schools, clinics and roads that benefit everyone, and paying them honestly is a democratic responsibility.", True]]},
 {"title": "Example 2: Calculate a simulated tax",
  "problem": "A simulated tax of <b>10%</b> is added to a purchase of <b>C$ 200</b>. What is the total?",
  "steps": [["Find the tax.", "200 × 10 ÷ 100 = 20."],
            ["Add it to the price.", "200 + 20 = 220."],
            ["Check the unit.", "C$ (simulated)."],
            ["Answer.", "The tax is C$ 20 and the total is <b>C$ 220</b>.", True]]},
 {"title": "Example 3: Share a community budget",
  "problem": "You have a simulated budget of 100%. Share it among <b>health, education, roads, water, security and environment</b>.",
  "steps": [["Read the needs.", "Which services are most urgent in your community?"],
            ["Choose priorities.", "For example health and education are first."],
            ["Assign percentages.", "Health 25, education 25, roads 15, water 15, security 10, environment 10 = 100."],
            ["Check the total.", "It must be exactly 100%."],
            ["Explain the biggest choices.", "“I gave 25% to education because it helps the whole community in the long term.”"],
            ["Final plan.", "A budget that adds up to 100% and explains the priorities with the benefits.", True]]},
 {"title": "Example 4: Write a short argument",
  "problem": "Write a short argument on how taxes contribute to the common good.",
  "steps": [["State the claim.", "“Taxes contribute to the common good.”"],
            ["Give a reason.", "“They pay for services that all people use.”"],
            ["Give an example.", "“Taxes help pay for schools, roads and health services.”"],
            ["Give a closing action.", "“So I should pay them honestly and demand transparency.”"],
            ["Final argument.", "<i>Taxes contribute to the common good because they pay for services that all people use, such as schools, roads and health services. So citizens should pay them honestly and ask for transparency in how they are used.</i>", True]]},
]

quiz = [
 Q("What is fiscal education?", ["A teaching and learning process that builds an active citizenry that understands the duty to pay taxes", "A class about money games", "A subject about trade only", "A school fee"], "It builds tax values and responsible citizens."),
 Q("What is taxation (tributación)?", ["Citizens give the State money so it can provide services such as education and health", "A tax on schools only", "Money lent to the State", "A fine"], "Taxation funds services for everyone."),
 Q("What is a tribute (tributo)?", ["A payment the State demands by law, including taxes, fees and contributions", "A gift", "A loan", "A private debt"], "Tributes must be set in legal norms."),
 Q("What is the taxing power (potestad tributaria)?", ["The State's faculty to create, modify or suppress tributes", "The power of citizens to avoid taxes", "The power of banks", "A school rule"], "It is the legal faculty to demand contributions."),
 Q("Which power exercises the taxing power?", ["The Legislative Power", "The Judicial Power only", "Any company", "The media"], "It is exercised by the Legislative Power, through law."),
 Q("What do taxes help to pay for?", ["Education, health, roads and security", "Private parties", "Personal debts", "Nothing in particular"], "Services that improve the country and the well-being of the population."),
 Q("How long is a budget usually valid?", ["One year", "One week", "Ten years", "One day"], "A budget covers a year."),
 Q("Why is the budget important?", ["It is the basis for transparency: we can know where public money goes", "It is secret", "It is only for the government", "It decides vacations"], "It allows evaluating the results of public management."),
 Q("Which is the correct order of the budget stages?", ["Formulation, discussion and approval, execution, control and evaluation", "Execution, control, formulation, approval", "Approval, formulation, control, execution", "Control, execution, approval, formulation"], "Four stages."),
 Q("A responsible citizen…", ["Pays taxes, cares for the environment and respects others' rights", "Only demands services", "Avoids rules", "Does not vote"], "Rights and duties go together."),
]

acts = [
 {"id": "act-quiz", "type": "quiz", "title": "Mastery Quiz (10 questions)", "intro": "Ten questions on taxes and the common good. Aim for 80% or higher.", "qs": quiz},
 {"id": "act-match", "type": "match", "title": "Match the Term", "intro": "Tap the term, then its meaning.",
  "pairs": [["Taxation", "Citizens give money to the State for services"], ["Tribute", "Payment demanded by law: taxes, fees, contributions"], ["Taxing power", "State's faculty to create, modify or suppress tributes"], ["Budget", "Plan of income, expenses and investments for a year"], ["Transparency", "Being able to see where public money goes"], ["Fiscal education", "Learning why taxes exist and why we pay them"], ["Citizenship", "Equality of rights and duties, freedom and responsibility"]]},
 {"id": "act-seq", "type": "seq", "title": "The Four Stages of the Budget", "intro": "Put the stages of the national budget in order.",
  "items": [{"t": "Formulation: estimate income and plan expenses", "hint": "The first step is to plan.", "why": "Planning comes first."},
            {"t": "Discussion and approval", "hint": "The plan is reviewed and approved.", "why": "The plan is discussed and approved."},
            {"t": "Execution: the money is spent as planned", "hint": "After approval.", "why": "Execution carries the plan out."},
            {"t": "Control and evaluation of the results", "hint": "The final stage.", "why": "Control shows whether the results are good."}]},
 {"id": "act-tf", "type": "sort", "title": "True or False: Taxing Power", "intro": "From your textbook activity: analyze the characteristics of the taxing power.",
  "choices": [{"k": "T", "label": "✅ True"}, {"k": "F", "label": "❌ False"}],
  "cards": [["It is inherent (natural) to the State.", "T", "The State needs it to exist and meet needs."], ["It emanates from the supreme norm (the Constitution).", "T", "It is based on the highest norm."], ["It is exercised by the Legislative Power.", "T", "Taxes are created by law."],
            ["It allows imposing contributions by means of law.", "T", "Contributions are set by law."], ["Any citizen may decide to create a new tax.", "F", "Only the State, by law."], ["Companies decide how much tax they want to pay.", "F", "Tributes are set by law."], ["It underpins the action of the authorities.", "T", "It gives authorities a basis to act."], ["Taxes can be created without any law.", "F", "A tribute must be set in legal norms."]]},
 {"id": "act-fund", "type": "sort", "title": "Public Service or Private Purchase?", "intro": "Is each item usually funded with <b>public money (taxes)</b> or is it a <b>private purchase</b>?",
  "choices": [{"k": "P", "label": "🏛 Public (taxes)"}, {"k": "V", "label": "🛍 Private purchase"}],
  "cards": [["The pay of teachers in a public school.", "P", "Education is a public service."], ["The repair of a public road.", "P", "Roads are built with public money."], ["Street lights in your neighborhood.", "P", "Public lighting is a public service."],
            ["A video game you buy.", "V", "It is a private purchase."], ["Medicine and staff in a public health center.", "P", "Health is a public service."], ["A pair of sneakers.", "V", "It is a private purchase."], ["A family's birthday party.", "V", "It is a private expense."], ["Waste collection in the town.", "P", "A public service."]]},
 {"id": "act-multi", "type": "multi", "title": "Select All That Apply", "intro": "Some questions have more than one right answer.",
  "qs": [{"q": "Which are public services that taxes help to pay for?", "o": ["Education", "Health", "Roads", "A friend's birthday party"], "a": [0, 1, 2], "e": "Private parties are not public services."},
         {"q": "Which belong to the budget?", "o": ["Expected income", "Planned expenses", "Investments", "Secret deals"], "a": [0, 1, 2], "e": "A budget should be transparent."},
         {"q": "Which are social values?", "o": ["Respect", "Honesty", "Justice", "Corruption"], "a": [0, 1, 2], "e": "Corruption is the opposite of a social value."},
         {"q": "A responsible citizen…", "o": ["Pays taxes", "Cares for the environment", "Respects others' rights", "Avoids all duties"], "a": [0, 1, 2], "e": "Responsible citizens fulfill their duties."}]},
 {"id": "act-calc", "type": "calc", "gen": "tax", "n": 5, "title": "Tax and Budget Numbers (your own set)", "rtitle": "Tax and budget numbers (simulated)",
  "intro": "Practice with simulated numbers. Each classmate gets different numbers."},
 {"id": "act-cloze", "type": "cloze", "title": "Complete the Sentences", "intro": "Choose the word that completes each sentence.",
  "items": [["Taxes help pay for education, health and ", ["roads", "parties", "toys"], 0, ".", "Public services."],
            ["The taxing power is exercised by the ", ["Legislative", "Private", "Foreign"], 0, " Power.", "Through law."],
            ["A budget is usually valid for one ", ["year", "day", "decade"], 0, ".", "It covers a year."],
            ["The budget is a basis for ", ["transparency", "secrecy", "luck"], 0, " in public spending.", "We can know where the money goes."],
            ["Paying taxes honestly is a democratic ", ["responsibility", "choice only", "game"], 0, ".", "It is a duty of citizens."],
            ["Social values like honesty and justice form a ", ["chain", "wall", "sale"], 0, " of values.", "No value acts alone."]]},
 {"id": "act-scen", "type": "scenario", "title": "What Would You Do?", "intro": "Choose the best response in each situation.",
  "steps": [{"s": "A friend says: “Taxes are useless; I will never pay when I grow up.” What do you say?", "o": [
              {"t": "Explain that taxes pay for schools, clinics and roads that everyone uses, and that paying honestly is a responsibility.", "p": 2, "f": "You explain with examples and values."},
              {"t": "Agree, to avoid an argument.", "p": 0, "f": "That supports a harmful idea."},
              {"t": "Change the subject.", "p": 1, "f": "Avoiding it does not help the friend understand."}]},
            {"s": "A shop does not give a receipt and says it will be cheaper. What is the best reaction?", "o": [
              {"t": "Ask for the receipt and explain that sales and taxes should be recorded; if refused, tell an adult.", "p": 2, "f": "You promote transparency."},
              {"t": "Accept it to save money.", "p": 0, "f": "Not recording a sale avoids taxes."},
              {"t": "Say nothing and leave.", "p": 1, "f": "You did not take part, but you could speak up."}]},
            {"s": "Your class has a small fund for activities. What is a transparent way to manage it?", "o": [
              {"t": "Write the income and expenses, share the report with the class and vote on priorities.", "p": 2, "f": "Budget + report + participation."},
              {"t": "Let one friend keep the money with no records.", "p": 0, "f": "Without records there is no transparency."},
              {"t": "Keep records but do not show them.", "p": 1, "f": "Records are good; sharing them builds trust."}]},
            {"s": "You see a broken public bench in the park. What is a responsible citizen to do?", "o": [
              {"t": "Report it to the proper authority and take care of public property.", "p": 2, "f": "Public property is paid for by everyone."},
              {"t": "Leave it; the government should notice.", "p": 0, "f": "Citizens take part by reporting."},
              {"t": "Tell your friends but not the authority.", "p": 1, "f": "Report it to those who can fix it."}]}]},
 {"id": "act-budget", "type": "alloc", "title": "Share the Community Budget", "rtitle": "Community budget simulation", "total": 100,
  "intro": "Imagine a community has a simulated budget of <b>100%</b>. Decide how much each service receives. The total must be exactly 100%. See Worked Example 3.",
  "items": [{"n": "Health", "hint": "Clinics, medicines, vaccination"}, {"n": "Education", "hint": "Schools, teachers, materials"}, {"n": "Roads and transport", "hint": "Streets, bridges, safe crossings"}, {"n": "Clean water and sanitation", "hint": "Water supply, drainage, waste collection"}, {"n": "Security", "hint": "Safe public spaces"}, {"n": "Environment and parks", "hint": "Trees, parks, recycling"}],
  "reason": "Explain your biggest choice and the benefit it brings to the community."},
 {"id": "act-values", "type": "open", "title": "Social Values Mini-Debate", "rtitle": "Social values and taxes", "min": 15,
  "intro": "From your textbook: choose <b>three</b> social values (peace, brotherhood, dignity, responsibility, respect, equality, cooperation or honesty) and connect each one with paying taxes or caring for public resources.",
  "prompts": [{"q": "1. Value 1: what it means and how it connects with taxes", "rows": 3}, {"q": "2. Value 2: what it means and how it connects with taxes", "rows": 3}, {"q": "3. Value 3: what it means and how it connects with taxes", "rows": 3}]},
 {"id": "act-arg", "type": "open", "title": "My Argument: Taxes and the Common Good", "rtitle": "Argument: taxes and the common good", "min": 40,
  "intro": "Write a short argument (4–6 sentences) about how taxes contribute to the common good of your family, school and community. See Worked Example 4.",
  "prompts": [{"q": "My argument (claim, reason, example, closing action):", "rows": 7}]},
 {"id": "act-book", "type": "open", "title": "Book Review Questions", "rtitle": "Review questions (Creciendo en Valores, pp. 112 and 115)", "min": 20,
  "intro": "From your textbook (Temas 17 and 18).",
  "prompts": [{"q": "1. What is taxation?", "rows": 3}, {"q": "2. Why is the tribute important?", "rows": 3}, {"q": "3. Explain what the taxing power is.", "rows": 3}, {"q": "4. What does citizenship mean, and why is education important for building it?", "rows": 3}, {"q": "5. Why is the preparation of the national budget important?", "rows": 3}]},
] + exit_acts(["1. Explain in your own words what taxes are for, with one example.", "2. Name the four stages of the budget and one social value connected with paying taxes."],
              "Write about five lines. Where do you see the results of public money (a school, a road, a clinic)? How can you take care of it?")

W = dict(
  slug="gv8-q2-week-7-taxes-and-the-common-good", week=7, short="Taxes and the Common Good",
  desc="Interactive study page for Growing in Values (8th grade, Q02 Week 7): fiscal education, taxes and the national budget, social values and the responsible citizen, with a budget simulation and practice.",
  eyebrow="Fiscal education · Taxes", title="Taxes and the Common Good",
  guiding="“How do taxes help my family, my school and my community?”",
  target="I can explain what taxes, tributes and the taxing power are, describe the stages of the budget, share a simulated budget with reasons, and argue how taxes contribute to the common good.",
  indicator="Values the importance of taxes in the common well-being of the family, the school and the community.",
  book="pp. 109–116", plan="Taxes and the common good (S1_U2_C07)",
  learn=learn, ideas=ideas, vocab=vocab, examples=examples, acts=acts, gens=GENS,
  method='<div class="card soft"><b>A short argument:</b> (1) Claim · (2) Reason · (3) Example · (4) Closing action.</div>',
  selfcheck=["I can explain what taxes are for.", "I can name the four stages of the budget.", "I can describe the characteristics of the taxing power.", "I completed my budget, my argument and my exit ticket."],
  motto="Honest contributions build a better community.")
