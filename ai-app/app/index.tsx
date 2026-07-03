import React, { useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";

type Message = {
  id: string;
  role: "user" | "assistant";
  text: string;
};

export default function ChatScreen() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      text: "👋 Hello! Ask me anything.",
    },
  ]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const question = message;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setMessage("");
    setLoading(true);

    try {
      // Replace with your laptop IP
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: question,
        }),
      });

      const data = await response.json();

      const aiMessage: Message = {
        id: Date.now().toString() + "_ai",
        role: "assistant",
        text: data.answer,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: Date.now().toString() + "_error",
        role: "assistant",
        text: "❌ Unable to connect to server.",
      };

      setMessages((prev) => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS == "ios" ? "padding" : undefined}
      >
        {/* Header */}

        <View style={styles.header}>
          <Text style={styles.headerTitle}>AI Assistant</Text>
          <Ionicons name="sparkles" size={24} color="#fff" />
        </View>

        {/* Chat */}

        <FlatList
          data={messages}
          keyExtractor={(item) => item.id}
          contentContainerStyle={{ padding: 15 }}
          renderItem={({ item }) => (
            <View
              style={[
                styles.messageContainer,
                item.role == "user"
                  ? styles.userContainer
                  : styles.aiContainer,
              ]}
            >
              <Text
                style={[
                  styles.messageText,
                  item.role == "user"
                    ? styles.userText
                    : styles.aiText,
                ]}
              >
                {item.text}
              </Text>
            </View>
          )}
        />

        {loading && (
          <View style={styles.loading}>
            <ActivityIndicator size="small" color="#10A37F" />
            <Text style={{ marginLeft: 10 }}>Thinking...</Text>
          </View>
        )}

        {/* Input */}

        <View style={styles.bottom}>
          <TextInput
            value={message}
            onChangeText={setMessage}
            placeholder="Type your message..."
            style={styles.input}
            multiline
          />

          <TouchableOpacity
            style={styles.sendButton}
            onPress={sendMessage}
          >
            <Ionicons
              name="send"
              size={22}
              color="#fff"
            />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F4F7FB",
  },

  header: {
    height: 70,
    backgroundColor: "#10A37F",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
    elevation: 5,
  },

  headerTitle: {
    color: "#fff",
    fontSize: 22,
    fontWeight: "bold",
  },

  messageContainer: {
    padding: 14,
    borderRadius: 18,
    marginBottom: 12,
    maxWidth: "80%",
  },

  userContainer: {
    alignSelf: "flex-end",
    backgroundColor: "#10A37F",
  },

  aiContainer: {
    alignSelf: "flex-start",
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#ddd",
  },

  messageText: {
    fontSize: 16,
    lineHeight: 24,
  },

  userText: {
    color: "#fff",
  },

  aiText: {
    color: "#111",
  },

  bottom: {
    flexDirection: "row",
    padding: 10,
    backgroundColor: "#fff",
    borderTopWidth: 1,
    borderColor: "#ddd",
    alignItems: "center",
  },

  input: {
    flex: 1,
    backgroundColor: "#F0F2F5",
    borderRadius: 25,
    paddingHorizontal: 18,
    paddingVertical: 10,
    maxHeight: 120,
    fontSize: 16,
  },

  sendButton: {
    marginLeft: 10,
    width: 52,
    height: 52,
    borderRadius: 26,
    backgroundColor: "#10A37F",
    justifyContent: "center",
    alignItems: "center",
  },

  loading: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 20,
    paddingBottom: 10,
  },
});