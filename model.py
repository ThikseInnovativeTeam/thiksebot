import nltk
import numpy as np
import pickle
from nltk.stem import PorterStemmer
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Downloading NLTK resources
nltk.download('punkt')

# Define the corpus and responses
corpus = [
    'Hi there! hi helo hello hii',
    'How are you?',
    'What is your name?',
    'Can you help me?',
    'I want your contact details.',
    'Where is your office located?',
    'How can I reach your HR department?',
    'Who is your founder and CEO?',
    'What is your founder name?',
    'When was the organization founded?',
    'How old are you?',
    'What is the weather like today?',
    'Goodbye!',
    'Bye',
]

responses = [
    'Hello! Happy to welcome you.',
    'I am fine, thank you!',
    'My name is Thiksebot.',
    'Yes, I can help you. What do you need?',
    'Contact number: +91 4146 358 357.',
    '746/D 2nd floor neruji road,villupuram 605602.',
    'For career-related tips, contact our HR at oviya@thikseservices.onmicrosoft.com.',
    'Krishnakanth is the founder and director of the organization.',
    'Krishnakanth is the founder and director of the organization.',
    'The organization started in 2024.',
    'I am a Thikse chatbot, so I do not have an age.',
    'The weather today is sunny with a chance of clouds.',
    'Goodbye!',
    'Goodbye!',
]

# Define corpus for drill-down responses
career_corpus = [
    'What career opportunities like IT, Non-IT, Data Entry, full stack developer, Front-End, Back-End, AI Developer, Python, JavaScript, HR, Digital Marketing',
    'IT, Non-IT, Data Entry, full stack developer, Front-End, Back-End, AI Developer, Python, JavaScript, HR, Digital Marketing',
    'How can I apply for a job?',
    'Do you offer internships?',
]

career_responses = [
    'We have various career opportunities available. Could you specify your field of interest?',
    'Send your Resume to our HR: oviya@thikseservices.onmicrosoft.com.',
    'You can apply for a job by visiting our careers page on our website.',
    'Yes, we offer internships. For more details, please visit our careers page.',
]

organization_corpus = [
    'what are the service Do you provide ',
    'what is organization name',
    'what is your company name',
    'your co-founder name?',
    'your Vice President VP name',
    'Tell me more about your organization.',
    'Who are founder ceo in your organization?',
    'What are the values of your organization?',
]

organization_responses = [
    'We Provide various services: Gen AI Solution\nApp Development\nWeb Development\nCyber Security Services\nDigital Marketing Solutions\nNon IT Services',
    'Our Organization name is "Thikse Software Solution PVT LTD"',
    'Our Organization name is "Thikse Software Solution PVT LTD"',
    "Our Co-Founder is Mr.Shiva\nAs a co-founder of Thikse Software Solutions, I drive our vision forward by fostering innovation and collaboration. I spearhead strategic initiatives, nurture our team's talents, and cultivate a culture of excellence. Together with my co-founders, I am passionate about delivering exceptional solutions to our clients.",
    "Our Vice President is Mrs.Malavika\nAs the Chief Financial Officer, I prioritize my responsibility by placing significant value on the engagement of our people and fostering a motivating environment. I actively support my leadership team in their aspirations and endeavors to achieve targets through effective management of funds and transactions.",
    'Our Mission: At Thikse Software Solutions, we\'re on a mission to empower talent and exceed client expectations. By championing fresh perspectives and securing exciting projects, we\'re building a dynamic community where innovation flourishes and success is inevitable.\n Our Vision: At Thikse Software Solutions, we prioritize quality and timely delivery while fostering our team\'s growth. Our commitment to excellence extends beyond projects—we\'re constantly innovating, expanding, and improving. Join us in creating a future where success knows no bounds.',
    'Our founder and director Mr.Krishnakanth, along with other talented professionals.',
    'Our values include integrity, teamwork, and customer satisfaction.',
]


# Combine all corpora
all_corpus = corpus + career_corpus + organization_corpus
all_responses = responses + career_responses + organization_responses

# Check if the lengths match
assert len(all_corpus) == len(all_responses), "The lengths of the corpus and responses do not match."

# Tokenize and stem the words in the new dataset
stemmer = PorterStemmer()
corpus_tokens = [nltk.word_tokenize(sentence.lower()) for sentence in all_corpus]
corpus_stemmed = [' '.join([stemmer.stem(token) for token in tokens]) for tokens in corpus_tokens]

# Define TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus_stemmed)

# Label encode responses
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(all_responses)

# Define neural network model
model = Sequential([
    Dense(128, input_shape=(X.shape[1],), activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(len(set(y)), activation='softmax'),
])

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

# Train the model
model.fit(X.toarray(), y, epochs=200, batch_size=8)

# Save the model and vectorizer
model.save('chatbot_model.h5')
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
