from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from datetime import datetime
from flask import Flask, request, send_file
from fpdf import FPDF
import io


# Initialize app
app = Flask(__name__)
CORS(app)

# Load your models and data
model = joblib.load("model.pkl")
symptom_columns = joblib.load("symptom_columns.pkl")
mapping2 = joblib.load("mapping2.pkl")
sclf = joblib.load('stacking_model.pkl')


# Your maga_dic should be defined in this file or loaded as pkl
# Example: maga_dic = joblib.load("maga_dic.pkl")

dic0= {
        "disease_name": "(Vertigo) Paroxysmal Positional Vertigo",
        "description": "Paroxysmal Positional Vertigo (PPV)...",
        "medication": ["Meclizine", "Diazepam"],
        "precautions": ["Avoid sudden head movements"],
        "things_to_do_now": ["Sit down immediately if you feel dizzy"],
        "diet_recommendation": {
        "vegetarian": ["Include iron-rich foods like spinach, beetroot, and lentils to support blood health", "Consume B-vitamin sources such as whole grains, nuts, and dairy products", "Stay well-hydrated with water, coconut water, and clear soups"],
        "non_vegetarian": ["Include lean meats like chicken or fish for protein and B vitamins", "Eggs (boiled or scrambled) for vitamin D and essential nutrients", "Pair meats with fiber sources like vegetables or whole grains"],
        "vegan": ["Focus on whole grains (quinoa, millet), lentils, and chickpeas for nutrients", "Add flaxseeds, chia seeds, and walnuts for healthy fats", "Ensure good hydration with herbal teas and infused water"]
    }
    },
dic1 = {
    "disease_name": "AIDS",
    "description": "AIDS (Acquired Immunodeficiency Syndrome) is a condition caused by the Human Immunodeficiency Virus (HIV), which severely compromises the immune system. It makes the body highly susceptible to infections and illnesses, leading to progressive health deterioration. AIDS develops during advanced stages of untreated HIV and remains a global health challenge due to its impact on affected individuals and communities.",
    "medication": ["Antiretroviral therapy (ART)", "Protease inhibitors (e.g., Ritonavir, Lopinavir)", "Nucleoside reverse transcriptase inhibitors (NRTIs)", "Non-nucleoside reverse transcriptase inhibitors (NNRTIs)"],
    "precautions": ["Practice safe sex", "Avoid sharing needles", "Regular HIV testing", "Follow ART regimen strictly"],
    "things_to_do_now": ["Consult an HIV specialist", "Get tested if exposed to risk factors", "Strengthen immunity with a balanced diet", "Join a support group for mental well-being"],
    "diet_recommendation": {
        "vegetarian": ["Eat high-protein foods like lentils, chickpeas, tofu, and paneer to support immune function", "Include plenty of fruits (oranges, papaya, guava) and vegetables (spinach, carrots) for vitamins and minerals", "Add nuts and seeds (almonds, sunflower seeds) for healthy fats and energy"],
        "non_vegetarian": ["Include lean meats like chicken and fish for high-quality protein", "Eggs and dairy products (milk, yogurt) for calcium and vitamin D", "Pair meats with fiber-rich vegetables and whole grains for better digestion"],
        "vegan": ["Focus on protein-rich foods like lentils, beans, chickpeas, and quinoa", "Eat colorful fruits and vegetables daily for antioxidants and vitamins", "Add flaxseeds, chia seeds, and walnuts for omega-3 fatty acids"]
    }
    }
dic2 = {
    "disease_name": "Acne",
    "description": "Acne is a skin condition where hair follicles become clogged with oil and dead skin cells, resulting in pimples, blackheads, whiteheads, or cysts. It often appears on the face, chest, back, and shoulders and is influenced by factors like hormones, genetics, and skin care habits. Commonly seen in teenagers, acne can persist into adulthood and varies in severity.",
    "medication": ["Benzoyl peroxide", "Salicylic acid", "Topical retinoids (e.g., Tretinoin)", "Oral antibiotics (e.g., Doxycycline, Minocycline)"],
    "precautions": ["Keep skin clean and hydrated", "Avoid touching your face", "Use non-comedogenic skincare products", "Reduce dairy and high-glycemic foods"],
    "things_to_do_now": ["Wash your face with a mild cleanser", "Apply prescribed acne treatment", "Avoid popping pimples", "Consult a dermatologist for severe acne"],
    "diet_recommendation": {
        "vegetarian": ["Eat plenty of fruits and vegetables rich in antioxidants (like carrots, spinach, and berries)", "Include zinc-rich foods like pumpkin seeds and chickpeas", "Reduce intake of refined carbs and sugar-heavy foods"],
        "non_vegetarian": ["Include lean proteins like chicken and fish to balance hormones", "Eat eggs and low-fat dairy in moderation (if tolerated)", "Pair meals with fiber-rich vegetables to support skin health"],
        "vegan": ["Focus on whole grains, legumes, and leafy greens for nutrients", "Add chia seeds, flaxseeds, and walnuts for omega-3s", "Avoid excessive processed vegan snacks high in sugar or refined flour"]
    }
    }
dic3 = {
    "disease_name": "Alcoholic Hepatitis",
    "description": "Alcoholic Hepatitis is an inflammatory condition of the liver caused by excessive alcohol consumption over time. It damages liver cells and impairs liver function, leading to symptoms such as jaundice, abdominal pain, nausea, and fatigue. The severity of alcoholic hepatitis can vary, with more severe cases posing significant health risks and affecting overall well-being.",
    "medication": ["Corticosteroids (e.g., Prednisolone)", "Pentoxifylline", "Liver-protective supplements (e.g., S-Adenosylmethionine)"],
    "precautions": ["Stop alcohol consumption immediately", "Maintain a balanced diet rich in vitamins", "Monitor liver function regularly", "Stay hydrated"],
    "things_to_do_now": ["Seek immediate medical attention", "Follow a liver-friendly diet", "Avoid medications that strain the liver", "Consider alcohol rehabilitation programs"],
    "diet_recommendation": {
        "vegetarian": ["Include high-protein foods like lentils, chickpeas, tofu, and paneer to support liver repair", "Eat fruits and vegetables rich in antioxidants (like papaya, oranges, spinach, and carrots)", "Use healthy fats like olive oil in moderation and avoid deep-fried foods"],
        "non_vegetarian": ["Include lean proteins like chicken or fish (steamed or grilled, not fried)", "Eggs (boiled or poached) for additional protein", "Pair proteins with fiber-rich vegetables and whole grains"],
        "vegan": ["Eat protein-rich foods like lentils, quinoa, and beans", "Include nuts and seeds (walnuts, chia, flaxseeds) for healthy fats", "Focus on fresh fruits and vegetables while avoiding processed vegan junk foods"]
    }}
dic4 = {
    "disease_name": "Allergy",
    "description": "An allergy is an immune system reaction to substances called allergens, which are typically harmless to most people. Common allergens include pollen, dust, certain foods, insect stings, or animal dander. Allergic reactions can manifest as sneezing, itching, skin rashes, or breathing difficulties and vary in severity depending on the individual's sensitivity. It affects daily life and requires awareness of triggers.",
    "medication": ["Antihistamines (e.g., Loratadine, Cetirizine)", "Decongestants", "Corticosteroids", "Epinephrine (for severe reactions)"],
    "precautions": ["Avoid known allergens", "Use air purifiers", "Wear masks in dusty environments", "Keep antihistamines handy"],
    "things_to_do_now": ["Take antihistamines if symptoms appear", "Seek immediate help for severe reactions", "Get an allergy test to identify triggers", "Follow an allergen-free diet if necessary"],
    "diet_recommendation": {
        "vegetarian": ["Include vitamin C-rich foods (like oranges, guavas, amla) to support the immune system", "Eat turmeric, ginger, and garlic which have natural anti-inflammatory properties", "Limit processed foods and additives that may trigger allergies"],
        "non_vegetarian": ["Include omega-3 rich fish (like salmon, mackerel) to help reduce inflammation", "Eggs (if not allergic) for added protein", "Balance meals with plenty of vegetables and whole grains"],
        "vegan": ["Focus on fruits and vegetables high in antioxidants (berries, spinach, bell peppers)", "Add flaxseeds, chia seeds, and walnuts for omega-3 fatty acids", "Choose whole, unprocessed foods and avoid artificial additives"]
    }}
dic5 = {
    "disease_name": "Arthritis",
    "description": "Arthritis refers to a group of conditions causing inflammation and stiffness in the joints, leading to pain and reduced mobility. Common types include osteoarthritis and rheumatoid arthritis, each with distinct causes and symptoms. Arthritis can affect one or multiple joints, often worsening over time, and significantly impacts the quality of life for those who experience it.",
    "medication": ["NSAIDs (e.g., Ibuprofen, Naproxen)", "Corticosteroids", "Disease-modifying antirheumatic drugs (DMARDs)", "Biologic agents"],
    "precautions": ["Maintain a healthy weight", "Exercise regularly but gently", "Apply heat or cold therapy", "Avoid excessive joint strain"],
    "things_to_do_now": ["Consult a rheumatologist", "Take pain relief medication if needed", "Follow a joint-friendly diet", "Perform low-impact exercises like swimming"],
    "diet_recommendation": {
    "vegetarian": [
        "Include anti-inflammatory foods like spinach, kale, and broccoli",
        "Eat nuts and seeds (almonds, walnuts, flaxseeds) for healthy fats",
        "Add turmeric and ginger to meals for natural anti-inflammatory benefits"
    ],
    "non_vegetarian": [
        "Include fatty fish (salmon, mackerel) rich in omega-3 to help reduce joint inflammation",
        "Eat lean poultry for high-quality protein",
        "Pair meats with fiber-rich vegetables to support overall health"
    ],
    "vegan": [
        "Focus on whole grains, legumes, and dark leafy greens for nutrients",
        "Add chia seeds, flaxseeds, and walnuts for omega-3 fatty acids",
        "Incorporate turmeric, ginger, and garlic for their anti-inflammatory properties"
    ]
}}
dic6 = {
    "disease_name": "Bronchial Asthma",
    "description": "Bronchial Asthma is a chronic respiratory condition characterized by inflammation and narrowing of the airways. This leads to episodes of wheezing, coughing, shortness of breath, and chest tightness, often triggered by allergens, exercise, or environmental factors. Asthma varies in severity and can significantly impact daily activities if not managed effectively. It is common worldwide and affects people of all ages.",
    "medication": ["Bronchodilators (e.g., Albuterol, Salmeterol)", "Corticosteroids (e.g., Budesonide, Fluticasone)", "Leukotriene modifiers", "Theophylline"],
    "precautions": ["Avoid allergens and irritants", "Use inhalers as prescribed", "Maintain indoor air quality", "Stay hydrated"],
    "things_to_do_now": ["Use a rescue inhaler if shortness of breath occurs", "Monitor peak flow levels", "Seek emergency care if symptoms worsen", "Stay away from smoke and strong odors"],
    "diet_recommendation": {
        "vegetarian": ["Eat antioxidant-rich fruits and vegetables (e.g., apples, oranges, spinach, broccoli) to reduce airway inflammation", "Include turmeric and ginger for their anti-inflammatory properties", "Avoid excessive intake of processed and fried foods"],
        "non_vegetarian": ["Include omega-3 rich fish like salmon and mackerel to reduce inflammation", "Choose lean poultry for protein", "Pair animal protein with plenty of vegetables and whole grains"],
        "vegan": ["Focus on fresh fruits and vegetables rich in vitamins C and E", "Add flaxseeds, chia seeds, and walnuts for plant-based omega-3s", "Use turmeric, garlic, and ginger for natural anti-inflammatory support"]
    }}
dic7 = {
    "disease_name": "Cervical Spondylosis",
    "description": "Cervical Spondylosis is a common age-related condition affecting the neck's spinal discs and joints. It results from wear and tear over time, leading to symptoms like neck pain, stiffness, and reduced mobility. In severe cases, it may cause nerve compression, resulting in tingling, weakness, or coordination issues. This condition is prevalent among older adults and progresses gradually.",
    "medication": ["NSAIDs", "Muscle relaxants", "Physical therapy", "Corticosteroid injections"],
    "precautions": ["Maintain good posture", "Do neck strengthening exercises", "Use a supportive pillow", "Avoid prolonged screen time"],
    "things_to_do_now": ["Apply heat or cold therapy", "Take pain relief medication", "Consult an orthopedic specialist", "Perform gentle neck stretches"],
    "diet_recommendation": {
        "vegetarian": ["Consume calcium-rich foods like paneer, tofu, and dairy to support bone health", "Include leafy greens like spinach and kale for vitamins and minerals", "Add nuts and seeds for healthy fats and joint support"],
        "non_vegetarian": ["Include fish (like salmon and sardines) for omega-3 fatty acids and bone health", "Eat lean meats and eggs for high-quality protein", "Pair with vegetables and whole grains for balanced nutrition"],
        "vegan": ["Focus on plant-based calcium sources like tofu, almonds, sesame seeds, and fortified plant milks", "Include leafy greens and whole grains for additional nutrients", "Add flaxseeds, chia seeds, and walnuts for anti-inflammatory benefits"]
    }}
dic8 = {
    "disease_name": "Chicken Pox",
    "description": "Chickenpox is a contagious viral infection caused by the varicella-zoster virus. Chickenpox is a highly contagious viral infection that causes an itchy skin rash with red spots or fluid-filled blisters, often starting on the chest, back, and face.It is usually accompanied by fever, fatigue, and body aches. The rash typically spreads across the body in stages. Chickenpox is easily transmitted through direct contact or airborne particles and generally resolves within a few weeks.",
    "medication": ["Antiviral drugs (e.g., Acyclovir)", "Antihistamines", "Calamine lotion", "Paracetamol for fever"],
    "precautions": ["Avoid scratching blisters", "Stay isolated to prevent spreading", "Keep skin cool and hydrated", "Maintain good hygiene"],
    "things_to_do_now": ["Take antiviral medication if prescribed", "Drink plenty of fluids", "Apply calamine lotion for itch relief", "Rest until symptoms subside"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat soft, easy-to-swallow foods like khichdi, vegetable soups, and boiled potatoes",
        "Include vitamin C-rich fruits like oranges and papaya to boost immunity",
        "Stay hydrated with coconut water and fresh fruit juices"
    ],
    "non_vegetarian": [
        "Include soft boiled eggs or chicken soup for protein and recovery",
        "Pair with easily digestible carbs like rice or oats",
        "Drink plenty of fluids like clear broths"
    ],
    "vegan": [
        "Consume soft foods like mashed sweet potatoes and rice porridge",
        "Include vitamin-rich fruits like papaya, watermelon, and kiwi",
        "Stay hydrated with coconut water, lemon water, and herbal teas"
    ]
}
}
dic9 = {
    "disease_name": "Chronic cholestasis",
    "description" : "Chronic cholestasis is a condition where bile flow from the liver is persistently impaired, leading to the accumulation of bile acids in the bloodstream. This can cause symptoms such as jaundice, itching, dark urine, and pale stools. Over time, it may result in liver inflammation, scarring, and nutrient absorption issues, significantly affecting overall health and well-being.",
    "medication" : [],
    "precautions": [],
    "things_to_do_now": [],
    "diet_recommendation": {
    "vegetarian": [
        "Include high-fiber foods like oats, whole grains, and fruits to aid digestion",
        "Use small amounts of healthy fats like olive oil (avoid excess fat)",
        "Eat vitamin K-rich foods (spinach, broccoli) to support liver function"
    ],
    "non_vegetarian": [
        "Include lean protein sources like chicken and fish (steamed or grilled)",
        "Avoid high-fat meats and fried foods",
        "Pair with fiber-rich vegetables and whole grains"
    ],
    "vegan": [
        "Focus on whole grains, lentils, and beans for protein and fiber",
        "Eat leafy greens for vitamins and minerals",
        "Limit fatty and processed vegan foods"
    ]
}
}
dic10 = {
    "disease_name": "Common Cold",
    "description" : "The common cold is a viral infection that primarily affects the upper respiratory tract, including the nose and throat. It is highly contagious and spreads through droplets or contact with contaminated surfaces. Symptoms often include a runny nose, sneezing, sore throat, mild cough, and fatigue. The condition is usually mild and resolves within a week.",
    "medication" : [],
    "precautions": [],
    "things_to_do_now": [],
    "diet_recommendation": {
    "vegetarian": [
        "Include warm vegetable soups and herbal teas for comfort",
        "Eat vitamin C-rich fruits like oranges and amla",
        "Add ginger, turmeric, and garlic to meals for natural relief"
    ],
    "non_vegetarian": [
        "Have chicken soup for its soothing and anti-inflammatory properties",
        "Include eggs for added protein",
        "Stay hydrated with warm broths and clear fluids"
    ],
    "vegan": [
        "Drink warm herbal teas and vegetable broths",
        "Eat citrus fruits, guava, and bell peppers for vitamin C",
        "Add turmeric, ginger, and garlic for immune support"
    ]
}
}
dic11 = {
    "disease_name": "Dengue",
    "description": "Dengue is a mosquito-borne viral infection caused by the dengue virus, transmitted primarily by Aedes mosquitoes. It is prevalent in tropical and subtropical regions. Symptoms include high fever, severe headache, joint and muscle pain, rash, and nausea. While many cases are mild, dengue can occasionally progress to severe forms, posing significant health risks. It remains a major public health concern globally.",
    "medication": ["Paracetamol for fever", "Intravenous fluids for dehydration","Platelet transfusion (if needed)"],
    "precautions": ["Use mosquito repellents", "Wear protective clothing", "Avoid stagnant water", "Rest and stay hydrated"],
    "things_to_do_now": ["Monitor platelet count regularly", "Drink plenty of fluids", "Avoid NSAIDs like aspirin", "Seek immediate medical care if symptoms worsen"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat papaya leaf juice (traditionally believed to help platelet count — consult doctor)",
        "Include pomegranate, kiwi, and oranges for vitamins and minerals",
        "Stay hydrated with coconut water, lemon water, and fruit juices"
    ],
    "non_vegetarian": [
        "Include boiled eggs and chicken soup for strength and protein",
        "Pair with soft rice or oats",
        "Focus on hydration with clear broths and fluids"
    ],
    "vegan": [
        "Consume hydrating fruits like watermelon, kiwi, and papaya",
        "Eat lentil soups for protein",
        "Stay hydrated with coconut water and fresh juices"
    ]
}
}
dic12 = {
    "disease_name": "Diabetes",
    "description": "Diabetes is a chronic metabolic disorder characterized by high blood sugar levels due to the body's inability to produce or effectively use insulin. It affects how the body processes glucose, leading to symptoms such as frequent urination, excessive thirst, fatigue, and blurred vision. Diabetes can result in long-term health complications if not properly managed.",
    "medication": ["Insulin therapy", "Metformin", "Sulfonylureas (e.g., Glipizide, Glyburide)", "SGLT2 inhibitors (e.g., Empagliflozin)"],
    "precautions": ["Monitor blood sugar levels regularly", "Follow a low-carb, high-fiber diet", "Exercise regularly", "Avoid excessive sugar intake"],
    "things_to_do_now": ["Check blood glucose levels", "Take prescribed medication on time", "Stay hydrated", "Consult a doctor if blood sugar remains high"],
    "diet_recommendation": {
    "vegetarian": [
        "Focus on whole grains (millets, oats), legumes, and vegetables",
        "Include nuts and seeds in moderation",
        "Avoid refined sugar and processed foods"
    ],
    "non_vegetarian": [
        "Include lean meats (chicken, fish) with plenty of vegetables",
        "Avoid processed meats and fried foods",
        "Pair proteins with high-fiber carbs like quinoa or brown rice"
    ],
    "vegan": [
        "Eat whole grains, legumes, and fresh vegetables",
        "Include flaxseeds and chia seeds for healthy fats",
        "Limit sugary vegan snacks and refined carbs"
    ]
}
}
dic13 = {
    "disease_name": "Dimorphic Hemorrhoids (Piles)",
    "description": "Hemorrhoids, commonly known as piles, are swollen blood vessels in the rectal or anal area. They can be internal (inside the rectum) or external (around the anus). Symptoms include pain, itching, swelling, and occasional bleeding during bowel movements. Hemorrhoids are often linked to factors like straining, prolonged sitting, or pregnancy, and they vary in severity and discomfort.",
    "medication": ["Topical ointments (e.g., Hydrocortisone)", "Pain relievers (e.g., Ibuprofen)", "Laxatives (for stool softening)", "Minimally invasive procedures (if necessary)"],
    "precautions": ["Eat a high-fiber diet", "Drink plenty of water", "Avoid prolonged sitting", "Practice good hygiene"],
    "things_to_do_now": ["Apply cold compress for pain relief", "Take sitz baths", "Use over-the-counter hemorrhoid creams", "Consult a doctor if symptoms persist"],
    "diet_recommendation": {
    "vegetarian": [
        "Include high-fiber foods like whole grains, fruits, and vegetables",
        "Stay hydrated with water, buttermilk, and coconut water",
        "Avoid spicy and fried foods"
    ],
    "non_vegetarian": [
        "Eat lean meats with high-fiber sides like salads or whole grains",
        "Focus on hydration with broths and water",
        "Limit red meat and fried foods"
    ],
    "vegan": [
        "Consume high-fiber foods like lentils, beans, and whole grains",
        "Eat plenty of fresh fruits and vegetables",
        "Stay well hydrated and avoid processed snacks"
    ]
}
}
dic14 = {
    "disease_name": "Drug Reaction",
    "description": "A drug reaction refers to an unintended and harmful response to a medication when taken at standard doses. These reactions can range from mild symptoms like rashes or nausea to severe complications affecting organs or bodily functions. Drug reactions may result from individual sensitivities, incorrect dosages, or interactions with other substances, highlighting the importance of careful medication use.",
    "medication": ["Antihistamines (e.g., Diphenhydramine)", "Corticosteroids (for severe reactions)", "Epinephrine (for anaphylaxis)"],
    "precautions": ["Avoid known allergens", "Inform doctors about previous reactions", "Read medication labels carefully", "Monitor for any unusual symptoms"],
    "things_to_do_now": ["Discontinue the suspected medication", "Take antihistamines for mild reactions", "Seek emergency care for severe reactions", "Report the reaction to a healthcare provider"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat bland, easy-to-digest foods like rice and dal",
        "Stay hydrated with coconut water and fruit juices",
        "Include antioxidant-rich fruits and vegetables (spinach, carrots)"
    ],
    "non_vegetarian": [
        "Include soft boiled eggs or chicken broth",
        "Pair with plain rice or oats",
        "Focus on hydration and avoid spicy foods"
    ],
    "vegan": [
        "Consume soft, easy-to-digest foods like rice porridge and lentil soup",
        "Include fresh fruits for vitamins and hydration",
        "Stay hydrated with herbal teas and coconut water"
    ]
}
}
dic15 = {
    "disease_name": "Fungal Infection",
    "description": "Fungal infections, also known as mycoses, are caused by fungi that invade the skin, nails, or mucous membranes. They can also affect internal organs in severe cases. Common types include athlete's foot, ringworm, and yeast infections. Symptoms vary but often include itching, redness, and skin changes. Fungal infections are widespread and can be contagious, spreading through contact or environmental exposure.",
    "medication": ["Topical antifungal creams (e.g., Clotrimazole)", "Oral antifungals (e.g., Fluconazole)", "Antiseptic powders"],
    "precautions": ["Keep affected areas clean and dry", "Avoid sharing personal items", "Wear breathable fabrics", "Use antifungal soaps if prone to infections"],
    "things_to_do_now": ["Apply antifungal medication", "Avoid scratching the affected area", "Change damp clothing frequently", "Consult a doctor if infection spreads"],
    "diet_recommendation": {
    "vegetarian": [
        "Include garlic and turmeric in meals for natural antifungal benefits",
        "Eat fresh vegetables and whole grains",
        "Avoid excess sugar and refined carbs"
    ],
    "non_vegetarian": [
        "Include lean meats with plenty of vegetables",
        "Add garlic and ginger to meals",
        "Avoid processed meats and excess sugar"
    ],
    "vegan": [
        "Focus on whole foods like lentils, beans, and vegetables",
        "Include garlic, turmeric, and ginger regularly",
        "Limit sugary processed vegan snacks"
    ]
}
}
dic16 = {
    "disease_name": "GERD",
    "description": "Gastroesophageal Reflux Disease (GERD) is a chronic condition where stomach acid frequently flows back into the esophagus, causing irritation. Symptoms include heartburn, chest discomfort, regurgitation of food or sour liquid, and difficulty swallowing. GERD can significantly impact daily life and is often triggered by certain foods, lifestyle factors, or anatomical issues affecting the lower esophageal sphincter.",
    "medication": ["Proton pump inhibitors (e.g., Omeprazole)", "H2 blockers (e.g., Ranitidine)", "Antacids"],
    "precautions": ["Avoid spicy and acidic foods", "Eat smaller meals", "Do not lie down immediately after eating", "Elevate the head while sleeping"],
    "things_to_do_now": ["Take prescribed antacids", "Drink plenty of water", "Avoid smoking and alcohol", "Consult a doctor if symptoms persist"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat small, frequent meals with whole grains and vegetables",
        "Avoid spicy, fried, and acidic foods (like tomatoes, citrus)",
        "Include oats, bananas, and non-citrus fruits"
    ],
    "non_vegetarian": [
        "Choose lean meats like chicken and fish (grilled, not fried)",
        "Pair with non-acidic vegetables and whole grains",
        "Avoid fatty meats and spicy preparations"
    ],
    "vegan": [
        "Focus on oats, brown rice, and steamed vegetables",
        "Include bananas and melons as safe fruit options",
        "Avoid acidic foods, excess oil, and processed vegan foods"
    ]
}
}
dic17 = {
    "disease_name": "Gastroenteritis",
    "description": "Gastroenteritis is an inflammation of the stomach and intestines, commonly caused by viruses, bacteria, or parasites. It leads to symptoms like diarrhea, vomiting, abdominal cramps, and fever. Often referred to as \"stomach flu,\" it spreads easily through contaminated food, water, or close contact. Gastroenteritis can disrupt daily activities but usually resolves within a few days.",
    "medication": ["Oral rehydration salts (ORS)", "Antidiarrheal medications", "Probiotics"],
    "precautions": ["Stay hydrated", "Wash hands frequently", "Avoid contaminated food and water", "Rest and recover fully"],
    "things_to_do_now": ["Drink ORS to prevent dehydration", "Eat bland foods (e.g., rice, toast)", "Avoid dairy and fatty foods", "Seek medical help if symptoms worsen"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat light foods like rice porridge, boiled potatoes, and bananas",
        "Stay hydrated with ORS, coconut water, and clear vegetable soups",
        "Avoid dairy, fried, and spicy foods until recovery"
    ],
    "non_vegetarian": [
        "Consume clear chicken broth for gentle nourishment",
        "Include soft-boiled eggs if tolerated",
        "Focus on hydration and light, non-greasy foods"
    ],
    "vegan": [
        "Rice porridge, boiled carrots, and bananas are easy on the stomach",
        "Stay hydrated with coconut water and rice water",
        "Avoid fatty or processed foods during recovery"
    ]
}
}
dic18 = {
    "disease_name": "Heart Attack",
    "description": "A heart attack, or myocardial infarction, occurs when blood flow to the heart is blocked, often due to a buildup of fatty deposits (plaques) in the coronary arteries. This blockage damages heart muscle tissue, leading to symptoms like chest pain, shortness of breath, nausea, and fatigue. It is a serious medical condition requiring immediate attention to prevent severe complications.",
    "medication": ["Aspirin", "Nitroglycerin", "Beta-blockers", "Clot-busting drugs (Thrombolytics)"],
    "precautions": ["Maintain a heart-healthy diet", "Exercise regularly", "Control blood pressure and cholesterol", "Avoid smoking and excessive alcohol"],
    "things_to_do_now": ["Call emergency services immediately", "Chew aspirin (if recommended by a doctor)", "Stay calm and avoid exertion", "Follow-up with a cardiologist"],
    "diet_recommendation": {
    "vegetarian": [
        "Focus on whole grains, fruits, vegetables, and legumes",
        "Include nuts (almonds, walnuts) in moderation for heart-healthy fats",
        "Limit salt, sugar, and processed foods"
    ],
    "non_vegetarian": [
        "Eat lean meats like skinless chicken or fish (grilled or baked)",
        "Include omega-3-rich fish like salmon and mackerel",
        "Avoid red meat and fried foods"
    ],
    "vegan": [
        "Choose whole grains, beans, lentils, and fresh produce",
        "Add chia seeds and flaxseeds for omega-3s",
        "Limit processed vegan snacks high in salt or sugar"
    ]
}
}
dic19 = {
    "disease_name": "Hepatitis B",
    "description": "Hepatitis B is a viral infection that targets the liver, caused by the Hepatitis B Virus (HBV). It can lead to both acute and chronic liver conditions, with symptoms such as jaundice, fatigue, abdominal pain, and dark urine. Transmission occurs through contact with infected body fluids, including blood, saliva, and semen. Hepatitis B remains a significant global health concern.",
    "medication": ["Antiviral medications (e.g., Entecavir, Tenofovir)", "Interferon injections", "Liver-supportive supplements"],
    "precautions": ["Avoid alcohol and liver-toxic medications", "Practice safe hygiene and vaccination", "Monitor liver function regularly", "Follow a liver-friendly diet"],
    "things_to_do_now": ["Get tested for hepatitis markers", "Avoid sharing personal hygiene items", "Consult a hepatologist for further management", "Maintain a healthy lifestyle"],
    "diet_recommendation": {
    "vegetarian": [
        "Include whole grains, fruits, and vegetables for liver support",
        "Eat small, frequent meals to reduce liver strain",
        "Avoid oily, spicy, and processed foods"
    ],
    "non_vegetarian": [
        "Choose lean protein like chicken or fish (steamed or grilled)",
        "Pair with high-fiber foods like brown rice or veggies",
        "Avoid fatty meats and alcohol"
    ],
    "vegan": [
        "Focus on lentils, beans, and whole grains",
        "Eat plenty of fresh fruits and vegetables",
        "Limit processed foods and unhealthy fats"
    ]
}
}
dic20 = {
    "disease_name": "Hepatitis C",
    "description": "Hepatitis C is a viral infection that causes inflammation of the liver, potentially leading to serious liver damage over time. It is primarily transmitted through contact with infected blood, often via shared needles, unscreened blood transfusions, or unsafe medical practices. Symptoms may include jaundice, fatigue, abdominal pain, and dark urine, though many cases remain asymptomatic for years.",
    "medication": ["Direct-acting antivirals (e.g., Sofosbuvir, Ledipasvir)", "Interferon therapy"],
    "precautions": ["Avoid alcohol", "Practice safe hygiene", "Get regular liver function tests", "Avoid sharing needles"],
    "things_to_do_now": ["Get screened for hepatitis C", "Follow prescribed antiviral therapy", "Monitor liver health", "Consult a liver specialist"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat nutrient-dense foods like leafy greens, fruits, and whole grains",
        "Include turmeric and garlic for their potential liver benefits",
        "Avoid excess sugar and fried foods"
    ],
    "non_vegetarian": [
        "Include lean chicken and fish",
        "Pair with vegetables and whole grains",
        "Avoid red meat and fatty foods"
    ],
    "vegan": [
        "Eat beans, lentils, quinoa, and vegetables",
        "Add seeds (flax, chia) for healthy fats",
        "Avoid sugary or processed vegan snacks"
    ]
}
}
dic21 = {
    "disease_name": "Hepatitis D",
    "description": "Hepatitis D, also known as delta hepatitis, is a liver infection caused by the Hepatitis D Virus (HDV). It requires the presence of Hepatitis B Virus (HBV) to replicate and infect. HDV can lead to severe liver inflammation and complications, including cirrhosis and liver failure. Transmission occurs through contact with infected blood or body fluids, making it a serious health concern.",
    "medication": ["Interferon therapy", "Liver-protective supplements", "Antiviral medications (if coinfected with hepatitis B)"],
    "precautions": ["Avoid alcohol and liver-toxic drugs", "Get vaccinated against hepatitis B", "Practice safe hygiene", "Monitor liver function regularly"],
    "things_to_do_now": ["Consult a hepatologist", "Get tested for hepatitis markers", "Follow a liver-friendly diet", "Avoid sharing personal items"],
    "diet_recommendation": {
    "vegetarian": [
        "Consume fresh fruits, vegetables, and whole grains",
        "Stay hydrated and avoid processed, oily foods",
        "Include small amounts of healthy fats like olive oil"
    ],
    "non_vegetarian": [
        "Choose lean meats and fish",
        "Pair with fiber-rich sides",
        "Avoid alcohol and fatty foods"
    ],
    "vegan": [
        "Focus on whole foods like lentils, beans, and veggies",
        "Add seeds and nuts in moderation",
        "Limit processed and high-fat vegan items"
    ]
}
}
dic22 = {
    "disease_name": "Hepatitis E",
    "description": "Hepatitis E is a viral infection caused by the Hepatitis E Virus (HEV), primarily transmitted through contaminated water or food. It leads to liver inflammation and symptoms such as jaundice, fatigue, nausea, and abdominal pain. The condition is more common in areas with poor sanitation and typically resolves on its own, though severe cases can occur in vulnerable individuals.",
    "medication": ["Supportive care (rest, hydration)", "Antiemetics for nausea", "Liver-protective supplements"],
    "precautions": ["Drink clean, filtered water", "Maintain proper hygiene", "Avoid undercooked food", "Follow a balanced diet"],
    "things_to_do_now": ["Rest and stay hydrated", "Avoid alcohol consumption", "Eat light and nutritious meals", "Consult a doctor if symptoms worsen"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat light meals — rice, dal, steamed veggies",
        "Stay hydrated with coconut water, lemon water",
        "Avoid spicy, oily foods"
    ],
    "non_vegetarian": [
        "Focus on light soups like chicken broth",
        "Avoid heavy, fatty meats",
        "Include small portions of lean chicken if tolerated"
    ],
    "vegan": [
        "Rice, lentil soup, and boiled vegetables work well",
        "Stay hydrated with ORS and coconut water",
        "Avoid fried and processed foods"
    ]
}
}
dic23 = {
    "disease_name": "Hypertension",
    "description": "Hypertension, or high blood pressure, is a condition in which the force of blood against the artery walls is consistently elevated. It often develops over time and may not show symptoms initially, earning it the nickname \"silent killer.\" If left unmanaged, hypertension can lead to serious complications like heart disease, stroke, or kidney damage, affecting overall health and longevity.",
    "medication": ["ACE inhibitors (e.g., Lisinopril, Enalapril)", "Beta-blockers (e.g., Metoprolol, Atenolol)", "Calcium channel blockers (e.g., Amlodipine, Diltiazem)", "Diuretics (e.g., Hydrochlorothiazide, Chlorthalidone)", "Angiotensin II receptor blockers (e.g., Losartan, Valsartan)"],
    "precautions": ["Reduce sodium intake", "Exercise regularly", "Maintain a healthy weight", "Manage stress effectively", "Limit alcohol consumption", "Quit smoking"],
    "things_to_do_now": ["Check your blood pressure regularly", "Follow a low-sodium, heart-healthy diet", "Stay hydrated and avoid excessive caffeine",  "Take prescribed medications as directed", "Consult a doctor if blood pressure remains high"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat fruits, vegetables, whole grains, and low-fat dairy",
        "Include potassium-rich foods like bananas and spinach",
        "Limit salt and processed foods"
    ],
    "non_vegetarian": [
        "Choose lean poultry and fish",
        "Avoid processed meats and excessive salt",
        "Pair proteins with plenty of vegetables"
    ],
    "vegan": [
        "Focus on fresh fruits, vegetables, whole grains, and legumes",
        "Add flaxseeds and chia seeds for heart health",
        "Limit salty snacks and processed vegan foods"
    ]
}
}
dic24 = {
    "disease_name": "Hyperthyroidism",
    "description": "Hyperthyroidism is a condition where the thyroid gland produces an excessive amount of thyroid hormones. This hormonal imbalance accelerates the body's metabolism, leading to symptoms such as rapid heartbeat, weight loss, increased appetite, sweating, anxiety, and fatigue. It can affect various bodily functions and is more commonly observed in women than men.",
    "medication": ["Antithyroid drugs (e.g., Methimazole, Propylthiouracil)", "Beta-blockers for symptom control", "Radioactive iodine therapy"],
    "precautions": ["Monitor thyroid hormone levels", "Avoid excessive iodine intake", "Manage stress effectively", "Maintain a healthy diet"],
    "things_to_do_now": ["Get thyroid function tests", "Follow prescribed medication", "Avoid caffeine and stimulants", "Consult an endocrinologist"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat cruciferous vegetables (broccoli, cabbage) which may help slow thyroid hormone production",
        "Include whole grains and dairy for balanced nutrition",
        "Limit caffeine and spicy foods"
    ],
    "non_vegetarian": [
        "Include lean protein sources like chicken or fish",
        "Pair with whole grains and plenty of vegetables",
        "Avoid excessive iodine-rich seafood"
    ],
    "vegan": [
        "Focus on whole grains, cruciferous vegetables, and legumes",
        "Add seeds and nuts in moderation",
        "Limit processed and overly salty vegan foods"
    ]
}
}
dic25 = {
    "disease_name": "Hypoglycemia",
    "description": "Hypoglycemia occurs when blood sugar levels drop below normal, leading to symptoms such as shakiness, sweating, confusion, dizziness, and irritability. It can result from prolonged fasting, excessive physical activity, or certain medical conditions. Severe hypoglycemia can cause fainting or seizures, requiring prompt attention to restore blood sugar balance.",
    "medication": ["Glucose tablets or gel", "Fast-acting carbohydrates (e.g., juice, candy)", "Glucagon injection (for severe cases)"],
    "precautions": ["Monitor blood sugar regularly", "Eat small, frequent meals", "Avoid excessive insulin or diabetes medications", "Carry sugar sources at all times"],
    "things_to_do_now": ["Consume a fast-acting sugar source", "Recheck blood sugar after 15 minutes", "Eat a balanced meal to stabilize levels", "Seek medical help if symptoms persist"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat small, frequent meals with complex carbs (whole grains, fruits)",
        "Include nuts and seeds for healthy fats",
        "Avoid sugary snacks that cause rapid spikes and drops"
    ],
    "non_vegetarian": [
        "Include lean protein (chicken, fish) with complex carbs",
        "Pair meals with fiber-rich sides",
        "Avoid processed meats and sugary foods"
    ],
    "vegan": [
        "Focus on whole grains, lentils, and beans",
        "Include nuts and seeds for sustained energy",
        "Limit processed vegan sweets"
    ]
}
}
dic26 = {
    "disease_name": "Hypothyroidism",
    "description": "Hypothyroidism is a condition in which the thyroid gland produces insufficient amounts of thyroid hormones. This hormonal deficiency slows down metabolism, leading to symptoms such as fatigue, weight gain, cold intolerance, dry skin, hair thinning, depression, and constipation. It is a common endocrine disorder, often more prevalent in women, and can be managed with proper medical treatment.",
    "medication": ["Levothyroxine (thyroid hormone replacement)"],
    "precautions": ["Monitor thyroid levels regularly", "Follow a healthy, iodine-rich diet", "Exercise to manage weight", "Avoid processed and goitrogenic foods"],
    "things_to_do_now": ["Take prescribed medication daily", "Get thyroid function tests", "Maintain a balanced diet", "Consult an endocrinologist if symptoms persist"],
    "diet_recommendation": {
    "vegetarian": [
        "Include iodine-rich foods like dairy and iodized salt",
        "Eat whole grains, fruits, and vegetables",
        "Limit soy and cruciferous vegetables in large amounts"
    ],
    "non_vegetarian": [
        "Include lean meats, fish, and eggs",
        "Pair with high-fiber foods",
        "Use iodized salt in moderation"
    ],
    "vegan": [
        "Focus on seaweed (nori, wakame) in moderation for iodine",
        "Eat whole grains, legumes, and fruits",
        "Limit excess soy products"
    ]
}
}
dic27 = {
    "disease_name": "Impetigo",
    "description": "Impetigo is a highly contagious bacterial skin infection that primarily affects children but can occur in adults as well. It usually starts as red sores or blisters, often around the nose, mouth, or other exposed areas of the skin. These sores can burst, ooze, and form honey-colored crusts. Impetigo is caused by bacteria like Staphylococcus aureus or Streptococcus pyogenes and spreads through direct contact or shared items like towels or clothing.",
    "medication": ["Topical antibiotics (e.g., Mupirocin)", "Oral antibiotics (for severe cases)"],
    "precautions": ["Maintain good hygiene", "Avoid touching affected areas", "Wash hands frequently", "Keep sores covered to prevent spread"],
    "things_to_do_now": ["Apply prescribed antibiotic cream", "Keep affected area clean and dry", "Avoid scratching the sores", "Consult a doctor if infection worsens"],
    "diet_recommendation": {
    "vegetarian": [
        "Include vitamin C-rich fruits to promote healing",
        "Eat whole grains and vegetables for overall health",
        "Stay hydrated and avoid sugary snacks"
    ],
    "non_vegetarian": [
        "Include lean meats with plenty of vegetables",
        "Eat eggs for added protein",
        "Focus on hydration"
    ],
    "vegan": [
        "Eat fresh fruits, vegetables, and whole grains",
        "Include plant-based protein sources like lentils and beans",
        "Stay hydrated and avoid processed foods"
    ]
}
}
dic28 = {
    "disease_name": "Jaundice",
    "description": "Jaundice is a condition where the skin, whites of the eyes, and mucous membranes turn yellow due to high levels of bilirubin in the blood. This yellowing often indicates liver dysfunction or other issues affecting bile production or elimination. Common causes include hepatitis, gallstones, liver cirrhosis, and hemolysis. Symptoms can also include fatigue, dark urine, and pale stools. It’s important to address the underlying cause for proper treatment.",
    "medication": ["Liver-supportive supplements", "Hydration therapy", "Antiviral or antibiotic treatment (if infection-related)"],
    "precautions": ["Avoid alcohol and hepatotoxic substances", "Follow a liver-friendly diet", "Get regular liver function tests", "Maintain proper hydration"],
    "things_to_do_now": ["Increase water intake", "Avoid fatty and processed foods", "Follow medical advice for underlying conditions", "Consult a doctor if symptoms worsen"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat soft, easily digestible foods like rice, dal, and boiled veggies",
        "Stay hydrated with coconut water and fresh fruit juices (without added sugar)",
        "Avoid oily, spicy, and fried foods"
    ],
    "non_vegetarian": [
        "Include clear chicken broth or soft-boiled eggs if tolerated",
        "Avoid red meat and fatty foods",
        "Focus on hydration"
    ],
    "vegan": [
        "Rice, lentils, and boiled vegetables are gentle on the liver",
        "Stay hydrated with coconut water and lemon water",
        "Avoid fatty or processed vegan foods"
    ]
}
}
dic29 = {
    "disease_name": "Malaria",
    "description": "Malaria is a mosquito-borne infectious disease caused by Plasmodium parasites. It is transmitted through the bite of infected female Anopheles mosquitoes. Symptoms include fever, chills, headache, muscle aches, and fatigue. Severe cases can lead to complications like anemia, jaundice, seizures, or even death. Malaria is prevalent in tropical and subtropical regions and remains a significant global health challenge.",
    "medication": ["Antimalarial drugs (e.g., Chloroquine, Artemisinin-based therapy)", "Fever-reducing medications"],
    "precautions": ["Use mosquito repellents", "Sleep under a mosquito net", "Avoid stagnant water", "Take prophylactic medication if traveling to endemic areas"],
    "things_to_do_now": ["Take prescribed antimalarial drugs", "Rest and stay hydrated", "Monitor fever and symptoms", "Seek immediate medical care if severe symptoms appear"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat energy-dense foods like rice, roti, and boiled potatoes",
        "Include fruits rich in vitamin C and iron (oranges, guava, pomegranate)",
        "Stay hydrated with coconut water and lemon water"
    ],
    "non_vegetarian": [
        "Include soft-boiled eggs and chicken soup for strength",
        "Pair with soft carbs like rice",
        "Stay hydrated with broths"
    ],
    "vegan": [
        "Include energy-dense foods like rice, lentil soup, and boiled potatoes",
        "Eat vitamin C-rich fruits to help iron absorption",
        "Stay hydrated with coconut water and herbal teas"
    ]
}
}
dic30 = {
    "disease_name": "Migraine",
    "description": "A migraine is a neurological condition that causes recurring and often intense headaches, typically on one side of the head. It may be accompanied by nausea, vomiting, and sensitivity to light and sound. Some individuals experience warning signs called \"aura,\" which can include visual disturbances, before the headache phase begins. Migraines can last for hours to days and may significantly impact daily life. Triggers often include stress, certain foods, hormonal changes, or lack of sleep.",
    "medication": ["Triptans (e.g., Sumatriptan)", "Pain relievers (e.g., Ibuprofen, Acetaminophen)", "Beta-blockers (for prevention)"],
    "precautions": ["Avoid known triggers (e.g., stress, certain foods)", "Maintain a regular sleep schedule", "Stay hydrated", "Practice relaxation techniques"],
    "things_to_do_now": ["Rest in a quiet, dark room", "Apply a cold compress to the head", "Take prescribed migraine medication", "Avoid caffeine and strong odors"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat magnesium-rich foods like spinach, pumpkin seeds, and almonds",
        "Include whole grains and fresh fruits",
        "Avoid trigger foods like chocolate, aged cheese, and excess caffeine"
    ],
    "non_vegetarian": [
        "Include lean poultry and fish",
        "Pair with fiber-rich veggies and whole grains",
        "Avoid processed meats and high-sodium foods"
    ],
    "vegan": [
        "Focus on whole grains, legumes, nuts, and seeds",
        "Include magnesium-rich foods like chia seeds and spinach",
        "Avoid processed vegan foods high in additives"
    ]
}
}
dic31 = {
    "disease_name": "Osteoarthritis",
    "description": "Osteoarthritis is a degenerative joint disease that occurs when the protective cartilage that cushions the ends of bones wears down over time. It commonly affects weight-bearing joints like the knees, hips, and spine, as well as the hands. Symptoms include joint pain, stiffness, swelling, and a reduced range of motion. Osteoarthritis is most prevalent among older individuals and can impact daily activities, though it is manageable with lifestyle changes, physical therapy, and medications.",
    "medication": ["Pain relievers (e.g., Acetaminophen, NSAIDs)", "Joint supplements (e.g., Glucosamine, Chondroitin)", "Corticosteroid injections (for severe cases)"],
    "precautions": ["Maintain a healthy weight", "Engage in low-impact exercises", "Use joint-supportive devices if needed", "Follow a balanced diet rich in omega-3 fatty acids"],
    "things_to_do_now": ["Apply heat or cold therapy to affected joints", "Perform gentle stretching exercises", "Take prescribed pain medications", "Consult a rheumatologist for treatment options"],
    "diet_recommendation": {
    "vegetarian": [
        "Include calcium-rich foods like low-fat dairy, tofu, and leafy greens",
        "Add turmeric, ginger for natural anti-inflammatory benefits",
        "Focus on whole grains, fruits, and vegetables"
    ],
    "non_vegetarian": [
        "Include oily fish (salmon, mackerel) for omega-3s",
        "Lean chicken for protein with lots of vegetables",
        "Avoid red meat and fried foods"
    ],
    "vegan": [
        "Eat calcium-fortified plant milk, tofu, and leafy greens",
        "Add flaxseeds and chia seeds for omega-3s",
        "Include turmeric, ginger in cooking"
    ]
}
}
dic32 = {
    "disease_name": "Paralysis (brain hemorrhage)",
    "description": "Paralysis due to a brain hemorrhage occurs when bleeding in the brain disrupts its normal function. A brain hemorrhage, also known as a cerebral hemorrhage, is a type of stroke caused by a ruptured blood vessel in the brain. This bleeding can compress brain tissue, leading to symptoms such as sudden weakness or numbness on one side of the body, difficulty speaking, loss of coordination, and severe headache.",
    "medication": ["Blood pressure medications (e.g., Labetalol, Nicardipine)", "Anticoagulants (if indicated)", "Physical therapy for rehabilitation"],
    "precautions": ["Monitor blood pressure regularly", "Follow a healthy diet", "Avoid smoking and excessive alcohol consumption", "Seek immediate medical care for stroke symptoms"],
    "things_to_do_now": ["Call emergency medical services immediately", "Ensure the patient remains stable", "Start rehabilitation therapy as soon as possible", "Follow up with a neurologist"],
    "diet_recommendation": {
    "vegetarian": [
        "Include soft, nutrient-rich foods like khichdi, dal, and boiled veggies",
        "Use healthy fats like olive oil in moderation",
        "Stay hydrated and include fiber to prevent constipation"
    ],
    "non_vegetarian": [
        "Include soft proteins like scrambled eggs, steamed fish",
        "Pair with soft carbs like mashed potatoes or rice",
        "Focus on hydration with broths"
    ],
    "vegan": [
        "Eat soft lentil soups, rice porridge, and mashed veggies",
        "Include flax or chia seeds for healthy fats",
        "Stay hydrated and maintain fiber intake"
    ]
}
}
dic33 = {
    "disease_name": "Peptic ulcer disease",
    "description": "Peptic ulcer disease involves the formation of open sores in the lining of the stomach or the upper part of the small intestine. These ulcers can cause symptoms like burning stomach pain, bloating, nausea, and heartburn. Common causes include infection with Helicobacter pylori bacteria and prolonged use of nonsteroidal anti-inflammatory drugs (NSAIDs). If untreated, complications like internal bleeding or perforation may arise.",
    "medication": ["Proton pump inhibitors (e.g., Omeprazole, Lansoprazole)", "H2 receptor blockers (e.g., Ranitidine, Famotidine)", "Antibiotics for H. pylori infection"],
    "precautions": ["Avoid spicy and acidic foods", "Limit NSAID use", "Manage stress effectively", "Avoid alcohol and smoking"],
    "things_to_do_now": ["Take prescribed medications regularly", "Eat small, frequent meals", "Avoid caffeine and carbonated drinks", "Consult a gastroenterologist if symptoms persist"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat small, frequent, non-spicy meals (oats, bananas, rice)",
        "Include non-acidic fruits like papaya and melon",
        "Avoid caffeine, spicy, and fried foods"
    ],
    "non_vegetarian": [
        "Include soft proteins like boiled eggs, steamed chicken",
        "Pair with rice or oats",
        "Avoid spicy or fried meats"
    ],
    "vegan": [
        "Eat rice porridge, lentil soup, and non-acidic fruits",
        "Avoid citrus, caffeine, and spicy foods",
        "Stay hydrated with water, coconut water"
    ]
}
}
dic34 = {
    "disease_name": "Pneumonia",
    "description": "Pneumonia is an infection that inflames the air sacs in one or both lungs, which may fill with fluid or pus. It can be caused by bacteria, viruses, or fungi. Common symptoms include cough with phlegm, fever, chills, chest pain, and difficulty breathing. Pneumonia can range from mild to severe and is more dangerous for infants, the elderly, or individuals with weakened immune systems. ",
    "medication": ["Antibiotics (for bacterial pneumonia)", "Antiviral drugs (for viral pneumonia)", "Fever reducers and pain relievers"],
    "precautions": ["Get vaccinated for pneumonia", "Maintain good hand hygiene", "Avoid exposure to pollutants and smoke", "Stay hydrated and rest"],
    "things_to_do_now": ["Take prescribed antibiotics or antivirals", "Use a humidifier to ease breathing", "Get plenty of rest and fluids", "Seek immediate care if breathing difficulty worsens"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat energy-rich foods like khichdi, soups, and fruits",
        "Include ginger and garlic for natural immunity",
        "Stay hydrated with warm fluids"
    ],
    "non_vegetarian": [
        "Include chicken soup and soft-boiled eggs",
        "Pair with soft carbs like rice or oats",
        "Focus on warm fluids for comfort"
    ],
    "vegan": [
        "Consume lentil soups, rice porridge, and steamed vegetables",
        "Include ginger, garlic, turmeric in cooking",
        "Stay hydrated with herbal teas and warm water"
    ]
}
}
dic35 = {
    "disease_name": "Psoriasis",
    "description": "Psoriasis is a chronic autoimmune skin condition that causes the rapid buildup of skin cells, leading to scaling on the skin's surface. Inflammation and redness around the affected areas are common. Symptoms include thick, silvery scales, dry skin patches, itching, and discomfort. Psoriasis can appear on various parts of the body, including the scalp, elbows, knees, and lower back. It is not contagious, but factors like stress, infections, or certain medications can trigger or worsen symptoms.",
    "medication": ["Topical corticosteroids", "Vitamin D analogs (e.g., Calcipotriol)", "Biologic treatments (e.g., Adalimumab, Infliximab)"],
    "precautions": ["Moisturize skin regularly", "Avoid triggers like stress and infections", "Follow a healthy diet", "Limit alcohol and tobacco use"],
    "things_to_do_now": ["Apply prescribed creams and ointments", "Use mild soaps and moisturizers", "Manage stress through relaxation techniques", "Consult a dermatologist for further treatment options"],
    "diet_recommendation": {
    "vegetarian": [
        "Include anti-inflammatory foods like flaxseeds, walnuts, and fresh veggies",
        "Eat plenty of fruits and whole grains",
        "Avoid processed, sugary, and fried foods"
    ],
    "non_vegetarian": [
        "Include oily fish for omega-3s",
        "Lean chicken with vegetables",
        "Avoid processed meats and excess red meat"
    ],
    "vegan": [
        "Eat flaxseeds, chia seeds, and fresh vegetables",
        "Focus on whole grains and fruits",
        "Limit processed vegan snacks"
    ]
}
}
dic36 = {
    "disease_name": "Tuberculosis",
    "description": "Tuberculosis (TB) is a contagious bacterial infection caused by Mycobacterium tuberculosis. It primarily affects the lungs but can also impact other parts of the body. TB spreads through airborne droplets when an infected person coughs, sneezes, or speaks. Symptoms of active TB include persistent cough (sometimes with blood), fever, night sweats, weight loss, and fatigue.",
    "medication": ["Isoniazid", "Rifampin", "Ethambutol", "Pyrazinamide"],
    "precautions": ["Complete the full course of medication", "Avoid close contact with others if infectious", "Follow a nutrient-rich diet", "Get regular follow-ups with a doctor"],
    "things_to_do_now": ["Start anti-TB medication immediately", "Ensure proper ventilation at home", "Wear a mask to prevent spread", "Follow up with a doctor for regular monitoring"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat high-protein foods like paneer, dals, and soya",
        "Include calorie-dense foods like nuts and seeds",
        "Drink milk or lassi for added nutrition"
    ],
    "non_vegetarian": [
        "Include eggs, chicken, and fish for protein",
        "Pair with whole grains and vegetables",
        "Focus on small, frequent meals"
    ],
    "vegan": [
        "Consume lentils, chickpeas, and tofu",
        "Add nuts, seeds, and plant oils for calories",
        "Eat small, frequent, nutrient-rich meals"
    ]
}
}
dic37 = {
    "disease_name": "Typhoid",
    "description": "Typhoid fever is a bacterial infection caused by Salmonella Typhi. It spreads through contaminated food or water and is more common in areas with poor sanitation. Symptoms include prolonged high fever, abdominal pain, weakness, headache, and sometimes a rash. If untreated, it can lead to severe complications like intestinal perforation or organ damage.",
    "medication": ["Antibiotics (e.g., Ciprofloxacin, Azithromycin)", "Fever reducers", "Oral rehydration solutions"],
    "precautions": ["Drink clean, purified water", "Maintain proper hygiene", "Avoid raw and undercooked food", "Get vaccinated for typhoid if at risk"],
    "things_to_do_now": ["Start antibiotic treatment", "Stay hydrated with fluids", "Eat light, digestible meals", "Consult a doctor if symptoms worsen"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat soft foods like rice, boiled potatoes, and vegetable soup",
        "Include fruit juices (without pulp) for energy",
        "Stay hydrated with ORS, coconut water"
    ],
    "non_vegetarian": [
        "Include clear chicken soup for strength",
        "Add soft-boiled eggs if tolerated",
        "Focus on hydration and soft carbs"
    ],
    "vegan": [
        "Rice porridge, lentil soup, and mashed veggies",
        "Coconut water, lemon water for hydration",
        "Avoid fried, spicy foods"
    ]
}
}
dic38 = {
    "disease_name": "Urinary tract infection",
    "description": "A urinary tract infection (UTI) is an infection that affects the urinary system, including the bladder, urethra, and kidneys. It's commonly caused by bacteria, such as Escherichia coli (E. coli), entering the urinary tract. Symptoms include a burning sensation during urination, frequent urge to urinate, cloudy or foul-smelling urine, and lower abdominal pain. In severe cases, UTIs can lead to kidney infections, which may cause fever, chills, and back pain.",
    "medication": ["Antibiotics (e.g., Nitrofurantoin, Ciprofloxacin)", "Pain relievers (e.g., Phenazopyridine)"],
    "precautions": ["Drink plenty of water", "Maintain good personal hygiene", "Avoid holding in urine for long periods", "Wear loose, breathable clothing"],
    "things_to_do_now": ["Start prescribed antibiotics", "Increase water intake", "Avoid caffeine and acidic foods", "Consult a doctor if symptoms persist"],
    "diet_recommendation": {
    "vegetarian": [
        "Drink plenty of water and coconut water",
        "Include vitamin C-rich fruits like oranges and amla",
        "Avoid caffeine and spicy foods"
    ],
    "non_vegetarian": [
        "Lean protein (chicken, fish) with veggies",
        "Focus on hydration with broths",
        "Avoid spicy and fatty meats"
    ],
    "vegan": [
        "Eat fresh fruits, veggies, and whole grains",
        "Drink water, coconut water, and herbal teas",
        "Avoid sugary and processed foods"
    ]
}
}
dic39 = {
    "disease_name": "Varicose veins",
    "description": "Varicose veins are enlarged, twisted veins that most commonly appear on the legs and feet. They occur when the valves in the veins weaken, causing blood to pool and the veins to swell. Symptoms can include aching, heaviness, swelling, and itching around the affected area. In severe cases, varicose veins may lead to skin changes or ulcers.",
    "medication": ["Compression therapy", "Pain relievers", "Sclerotherapy (in some cases)"],
    "precautions": ["Avoid prolonged standing", "Elevate legs when resting", "Exercise regularly", "Maintain a healthy weight"],
    "things_to_do_now": ["Wear compression stockings", "Avoid sitting or standing for long periods", "Engage in low-impact exercises", "Consult a vascular specialist if needed"],
    "diet_recommendation": {
    "vegetarian": [
        "Include fiber-rich foods to prevent constipation (whole grains, fruits)",
        "Eat vitamin C-rich foods to support blood vessel health",
        "Stay hydrated and maintain a healthy weight"
    ],
    "non_vegetarian": [
        "Lean chicken or fish paired with fiber-rich veggies",
        "Avoid processed meats and excess salt",
        "Include omega-3 rich fish occasionally"
    ],
    "vegan": [
        "Focus on fiber-rich foods (lentils, beans, fruits)",
        "Include flaxseeds and chia seeds for healthy fats",
        "Stay hydrated and limit processed foods"
    ]
}
}
dic40 = {
    "disease_name": "Hepatitis A",
    "description": "Hepatitis A is a viral infection that causes inflammation of the liver. It is primarily transmitted through the ingestion of contaminated food or water or through close contact with an infected person. Symptoms may include fatigue, nausea, abdominal pain, jaundice (yellowing of the skin and eyes), and dark urine. Unlike other forms of hepatitis, Hepatitis A does not lead to chronic liver disease and is usually self-limiting, resolving within a few weeks to months.",
    "medication": ["Supportive care (rest, hydration)", "Liver-supporting supplements"],
    "precautions": ["Drink clean, safe water", "Practice good hygiene", "Get vaccinated for hepatitis A", "Avoid alcohol and fatty foods"],
    "things_to_do_now": ["Rest and stay hydrated", "Eat a light, healthy diet", "Follow a liver-friendly lifestyle", "Consult a doctor for symptom management"],
    "diet_recommendation": {
    "vegetarian": [
        "Eat soft, light foods like khichdi, boiled potatoes",
        "Include fruits like papaya, banana",
        "Stay hydrated with coconut water, lemon water"
    ],
    "non_vegetarian": [
        "Include clear chicken broth or soft-boiled eggs",
        "Avoid red meat and fatty foods",
        "Focus on light, easily digestible meals"
    ],
    "vegan": [
        "Rice porridge, lentil soup, and boiled vegetables",
        "Hydrate with coconut water and herbal teas",
        "Avoid oily and processed foods"
    ]
}
}
    # Add all your other disease dicts (dic2, dic3, ..., dic40)

maga_dic = [dic0, dic1, dic2, dic3, dic4, dic5, dic6, dic7, dic8, dic9,
            dic10, dic11, dic12, dic13, dic14, dic15, dic16, dic17, dic18, dic19,
            dic20, dic21, dic22, dic23, dic24, dic25, dic26, dic27, dic28, dic29,
            dic30, dic31, dic32, dic33, dic34, dic35, dic36, dic37, dic38, dic39, dic40]

try:
    diet_model = joblib.load("diet_model.pkl")
    diet_mapping = joblib.load("diet_mapping.pkl")
except:
    diet_model = None
    diet_mapping = {0: 'Low_Carb', 1: 'Low_Sodium', 2: 'Balanced'}

def bmi_pred(bmi):
    if bmi <= 20:
        return [
            "Yoga (30 minutes, flexibility & strength)",
            "Light strength training (2-3x/week)",
            "Brisk walking (20-30 minutes)",
            "Pilates (20-30 minutes)"
        ]
    elif bmi <= 25:
        return [
            "Brisk walking (30-45 minutes)",
            "Cycling (moderate, 30 minutes)",
            "Bodyweight exercises (3x/week)",
            "Swimming (30-40 minutes)"
        ]
    else:
        return [
            "Walking (45-60 minutes)",
            "Elliptical (30 minutes)",
            "Low-impact HIIT (20-25 minutes)",
            "Resistance band exercises"
        ]
    
@app.route('/')
def home():
    return "✅ MediMuse Backend Running"

@app.route('/predict-text', methods=['POST'])
def predict_text():
    data = request.get_json()

    # Parse input
    symptoms_input = data.get("symptoms", "")
    # patient_name = data.get("patient_name", "Unknown")
    #print(symptoms_input)
    #symptoms_input = [s for s in symptoms_input]
    age = int(data.get("age", 0))
    weight = float(data.get("weight", 0))
    height = float(data.get("height", 1.0))  # meters
    gender = data.get("gender", "Other")

    from sentence_transformers import SentenceTransformer, util
    import mtranslate

    def translate_text(text, target_lang = 'en'):
        return mtranslate.translate(text, target_lang)
    
    model = SentenceTransformer('pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb')
    symptom_embeddings = model.encode(symptom_columns)


    indices = []
    vec = [0 for i in range(0, len(symptom_columns))]
    
    def match_synonyms(user_text, threshold=0.65):
        user_embedding = model.encode(user_text)
        matched_symptoms = []
        phrases = [p.strip() for p in user_text.split(',') if p.strip()]
        for phrase in phrases:
            phrase_embedding = model.encode(phrase)
            for i, symptom in enumerate(symptom_columns):
                similarity = util.cos_sim(phrase_embedding, symptom_embeddings[i]).item()
                if similarity >= threshold:
                    matched_symptoms.append(symptom)
                    indices.append(i)
        return matched_symptoms

    user_text = translate_text(symptoms_input, 'en')
    matched_symptoms = match_synonyms(user_text)
    print(f"Matched symptoms: {matched_symptoms}")

    for i in indices:
        vec[i] = 1

    symptom_vector = vec
    vec = np.array(symptom_vector).reshape(1, -1)
    print(f"Symptom vector: {vec}")

    # Predict disease (single top prediction)
    disease_index = sclf.predict(vec)[0]
    print(f"Predicted disease index: {disease_index}")

    if 0 <= disease_index < len(maga_dic):
        disease_details = maga_dic[disease_index]
    else:
        disease_details = {
            
            "disease_name": "Unknown",
            "description": "No description available.",
            "medication": [],
            "precautions": [],
            "things_to_do_now": [],
            "diet_recommendation": {
                "vegetarian": ["General vegetarian diet"],
                "non_vegetarian": ["General non-vegetarian diet"],
                "vegan": ["General vegan diet"]
            }
        }

    bmi = round(weight / (height ** 2), 2)
    bmi_category = (
        "Underweight" if bmi <= 20 else
        "Normal weight" if bmi <= 25 else
        "Overweight"
    )
    exercise_plan = bmi_pred(bmi)

    if diet_model:
        diet_features = np.zeros((1, 10))
        diet_features[0, 0] = age
        diet_features[0, 1] = weight
        diet_label = diet_model.predict(diet_features)[0]
        model_diet = diet_mapping.get(diet_label, "Balanced")
    else:
        model_diet = "Balanced"

    result = {
        # "patient_name": patient_name,
        "date": datetime.today().strftime("%d-%m-%Y"),
        "age": age,
        "gender": gender,
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "bmi_category": bmi_category,
        "exercise_recommendations": exercise_plan,
        "model_diet_recommendation": model_diet,
        "disease_details": {
            "disease_name": disease_details["disease_name"],
            "description": disease_details["description"],
            "medication": disease_details["medication"],
            "precautions": disease_details["precautions"],
            "things_to_do_now": disease_details["things_to_do_now"],
            "detailed_diet": disease_details.get("diet_recommendation", {
                "vegetarian": ["General vegetarian balanced diet"],
                "non_vegetarian": ["General non-vegetarian balanced diet"],
                "vegan": ["General vegan balanced diet"]
            })
        }
    }

    return jsonify(result)

@app.route('/download-prescription', methods=['POST'])
def download_prescription():
    data = request.get_json()
    result = data.get("result", {})

    from fpdf import FPDF
    import io

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, txt="MediMuse Prescription", ln=True, align="C")
    pdf.ln(10)

    # Basic details
    pdf.cell(200, 10, txt=f"Date: {result.get('date', '')}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {result.get('age', '')}  Gender: {result.get('gender', '')}", ln=True)
    pdf.cell(200, 10, txt=f"BMI: {result.get('bmi', '')} ({result.get('bmi_category', '')})", ln=True)
    pdf.cell(200, 10, txt=f"AI Diet Plan: {result.get('model_diet_recommendation', '')}", ln=True)
   
    pdf.ln(5)

    disease = result.get('disease_details', {})

    # Disease section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Disease: {disease.get('disease_name', '')}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, txt=f"Description: {disease.get('description', '')}")
    pdf.ln(5)

    # Medications
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Medications:", ln=True)
    pdf.set_font("Arial", '', 12)
    for med in disease.get('medication', []):
        pdf.multi_cell(0, 10, f"- {med}")
    pdf.ln(5)

    # Precautions
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Precautions:", ln=True)
    pdf.set_font("Arial", '', 12)
    for pre in disease.get('precautions', []):
        pdf.multi_cell(0, 10, f"- {pre}")
    pdf.ln(5)

    # Things to do now
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Things to Do Now:", ln=True)
    pdf.set_font("Arial", '', 12)
    for thing in disease.get('things_to_do_now', []):
        pdf.multi_cell(0, 10, f"- {thing}")
    pdf.ln(5)

    # Exercise recommendations
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Exercise Recommendations:", ln=True)
    pdf.set_font("Arial", '', 12)
    for ex in result.get('exercise_recommendations', []):
        pdf.multi_cell(0, 10, f"- {ex}")
    pdf.ln(5)

    # Detailed diet plan
    detailed_diet = disease.get('detailed_diet', {})
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Detailed Diet Plan:", ln=True)
    pdf.set_font("Arial", '', 12)

    for diet_type in ["vegetarian", "non_vegetarian", "vegan"]:
        items = detailed_diet.get(diet_type, [])
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 10, txt=f"{diet_type.capitalize()}:", ln=True)
        pdf.set_font("Arial", '', 12)
        for item in items:
            pdf.multi_cell(0, 10, f"- {item}")
        pdf.ln(2)

    # Finalize PDF
    pdf_bytes = pdf.output(dest='S').encode('latin1')

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='prescription.pdf'
    )


if __name__ == '__main__':
    app.run(debug=True)




