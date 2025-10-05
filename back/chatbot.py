from flask import Blueprint, request, jsonify, session
from back.system_utilities.dbmanage import get_db, User
from back.system_utilities.dbmanage import ChatHistory
from back.system_utilities.user import login_required
from langchain_ollama import OllamaLLM

chatbot_bp = Blueprint('chatbot', __name__)

# Initialize Ollama LLM here or import from main app if singleton needed
llm = OllamaLLM(model="gemma3:4b", temperature=0.7)

@chatbot_bp.route("/start", methods=["GET"])
@login_required
def chatbot_start():
    db = next(get_db())
    user_type = session.get("user_type")
    
    if user_type == 'instructor':
        opening_message = f"Hello, Professor {user_type}, I'm your AI assistant here to help you."
    elif user_type == 'student':
        opening_message = f"Hello, {user_type}, I'm your AI assistant here to help you."
    else:
        opening_message = "Hello, I'm your AI assistant here to help you."

    db.close()
    return opening_message

@chatbot_bp.route("/", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "")
    user_id = session.get("user_id", None)

    db = next(get_db())
    user_type = "guest"
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user_type = user.type

        # Store user message
        user_msg_entry = ChatHistory(user_id=user_id, message=user_message, is_user=1)
        db.add(user_msg_entry)
        db.commit()

        # Get last 10 chat history messages
        history_msgs = (db.query(ChatHistory)
                          .filter(ChatHistory.user_id == user_id)
                          .order_by(ChatHistory.timestamp.desc())
                          .limit(10)
                          .all())
        history_msgs.reverse()  # oldest first

        # Build prompt with history
        prompt = f"You are assisting a {user_type}. Provide helpful, concise tutoring responses without mentioning AI.\n"
        for msg in history_msgs:
            sender = "User" if msg.is_user else "Tutor"
            prompt += f"{sender}: {msg.message}\n"
        prompt += f"User: {user_message}\nTutor:"

        response = llm.invoke(prompt).replace("*", "").strip()

        # Store AI reply
        bot_msg_entry = ChatHistory(user_id=user_id, message=response, is_user=0)
        db.add(bot_msg_entry)
        db.commit()
    else:
        context = "You are assisting a guest. Provide concise and helpful responses without mentioning AI. Responsd only for theis: "
        response = llm.invoke(context + user_message).replace("*", "").strip()

    db.close()
    return jsonify({"reply": response})
