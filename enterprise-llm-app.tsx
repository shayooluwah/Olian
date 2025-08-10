import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Settings, Upload, Database, Shield, Menu, X, LogOut, Plus, MessageSquare } from 'lucide-react';

const EnterpriseLLMApp = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentView, setCurrentView] = useState('chat');
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedModel, setSelectedModel] = useState('gpt-4');
  const [conversations, setConversations] = useState([
    { id: 1, title: 'New Conversation', active: true }
  ]);
  const [activeConversation, setActiveConversation] = useState(1);
  
  // Authentication states
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [user, setUser] = useState(null);
  
  // Configuration states
  const [apiConfigs, setApiConfigs] = useState([
    { name: 'OpenAI GPT-4', endpoint: 'https://api.openai.com/v1/chat/completions', key: '', model: 'gpt-4' },
    { name: 'Claude', endpoint: 'https://api.anthropic.com/v1/messages', key: '', model: 'claude-3-opus' },
    { name: 'Local Model', endpoint: 'http://localhost:11434/api/generate', key: '', model: 'llama2' }
  ]);
  
  const messagesEndRef = useRef(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  
  useEffect(scrollToBottom, [messages]);
  
  const handleLogin = (e) => {
    e.preventDefault();
    // In a real app, this would authenticate with your backend
    setUser({ 
      username: loginForm.username, 
      role: 'admin',
      organization: 'Acme Corp'
    });
    setIsLoggedIn(true);
    setMessages([
      {
        id: 1,
        type: 'assistant',
        content: `Welcome to your Enterprise LLM Assistant! I'm ready to help with your work while keeping your data secure and private.`,
        timestamp: new Date()
      }
    ]);
  };
  
  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    setMessages([]);
    setConversations([{ id: 1, title: 'New Conversation', active: true }]);
    setLoginForm({ username: '', password: '' });
  };
  
  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    
    // Simulate API call to selected LLM
    setTimeout(() => {
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: `This is a simulated response from ${selectedModel}. In a real implementation, this would connect to your configured LLM API endpoint with your enterprise data context.\n\nYour message: "${userMessage.content}"\n\nI would process this using your organization's trained model and private knowledge base, ensuring data privacy and compliance with your security policies.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000);
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };
  
  const createNewConversation = () => {
    const newId = Math.max(...conversations.map(c => c.id)) + 1;
    const newConv = { id: newId, title: 'New Conversation', active: false };
    setConversations([...conversations, newConv]);
    setActiveConversation(newId);
    setMessages([]);
  };
  
  const switchConversation = (id) => {
    setConversations(prev => prev.map(c => ({ ...c, active: c.id === id })));
    setActiveConversation(id);
    // In a real app, load conversation history here
    setMessages([]);
  };
  
  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <Shield className="h-12 w-12 text-blue-600 mr-2" />
              <h1 className="text-2xl font-bold text-gray-900">Enterprise LLM</h1>
            </div>
            <p className="text-gray-600">Secure AI for your organization</p>
          </div>
          
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input
                type="text"
                value={loginForm.username}
                onChange={(e) => setLoginForm(prev => ({ ...prev, username: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your username"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={loginForm.password}
                onChange={(e) => setLoginForm(prev => ({ ...prev, password: e.target.value }))}
                onKeyPress={(e) => e.key === 'Enter' && handleLogin(e)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your password"
              />
            </div>
            
            <button
              onClick={handleLogin}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
            >
              Sign In
            </button>
          </div>
          
          <div className="mt-6 text-center text-sm text-gray-500">
            Demo credentials: any username/password
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 bg-white shadow-lg overflow-hidden`}>
        <div className="p-4 border-b">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-blue-600 mr-2" />
              <span className="font-bold text-gray-900">Enterprise LLM</span>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="p-1 hover:bg-gray-100 rounded"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
        
        <div className="p-4">
          <button
            onClick={createNewConversation}
            className="w-full flex items-center justify-center py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors mb-4"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Chat
          </button>
          
          <div className="space-y-2">
            {conversations.map(conv => (
              <button
                key={conv.id}
                onClick={() => switchConversation(conv.id)}
                className={`w-full text-left p-2 rounded-md flex items-center ${
                  activeConversation === conv.id ? 'bg-blue-50 text-blue-600' : 'hover:bg-gray-50'
                }`}
              >
                <MessageSquare className="h-4 w-4 mr-2" />
                {conv.title}
              </button>
            ))}
          </div>
        </div>
        
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t bg-white">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600">{user.username}</span>
            <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
              {user.organization}
            </span>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setCurrentView('settings')}
              className="flex-1 p-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-md flex items-center justify-center"
            >
              <Settings className="h-4 w-4 mr-1" />
              Settings
            </button>
            <button
              onClick={handleLogout}
              className="flex-1 p-2 text-sm bg-red-100 hover:bg-red-200 text-red-600 rounded-md flex items-center justify-center"
            >
              <LogOut className="h-4 w-4 mr-1" />
              Logout
            </button>
          </div>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white shadow-sm p-4 flex items-center justify-between">
          <div className="flex items-center">
            {!sidebarOpen && (
              <button
                onClick={() => setSidebarOpen(true)}
                className="p-2 hover:bg-gray-100 rounded-md mr-4"
              >
                <Menu className="h-5 w-5" />
              </button>
            )}
            <h2 className="text-xl font-semibold text-gray-900">
              {currentView === 'chat' ? 'AI Assistant' : 'Configuration'}
            </h2>
          </div>
          
          {currentView === 'chat' && (
            <div className="flex items-center space-x-4">
              <select
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="gpt-4">GPT-4</option>
                <option value="claude-3">Claude 3</option>
                <option value="local-model">Local Model</option>
              </select>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setCurrentView('chat')}
                  className={`p-2 rounded-md ${currentView === 'chat' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'}`}
                >
                  <MessageSquare className="h-5 w-5" />
                </button>
                <button
                  onClick={() => setCurrentView('settings')}
                  className={`p-2 rounded-md ${currentView === 'settings' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'}`}
                >
                  <Settings className="h-5 w-5" />
                </button>
              </div>
            </div>
          )}
        </div>
        
        {/* Chat View */}
        {currentView === 'chat' && (
          <>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex max-w-3xl ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                    <div className={`flex-shrink-0 ${message.type === 'user' ? 'ml-3' : 'mr-3'}`}>
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        message.type === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'
                      }`}>
                        {message.type === 'user' ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                      </div>
                    </div>
                    <div className={`px-4 py-2 rounded-lg ${
                      message.type === 'user' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-white border shadow-sm'
                    }`}>
                      <div className="whitespace-pre-wrap">{message.content}</div>
                      <div className={`text-xs mt-1 ${
                        message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                      }`}>
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="flex max-w-3xl">
                    <div className="flex-shrink-0 mr-3">
                      <div className="w-8 h-8 rounded-full flex items-center justify-center bg-gray-200 text-gray-600">
                        <Bot className="h-4 w-4" />
                      </div>
                    </div>
                    <div className="px-4 py-2 rounded-lg bg-white border shadow-sm">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
            
            <div className="p-4 bg-white border-t">
              <div className="flex items-end space-x-4">
                <div className="flex-1">
                  <textarea
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message... (Press Enter to send)"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                    rows="1"
                    style={{ minHeight: '44px', maxHeight: '120px' }}
                  />
                </div>
                <button
                  onClick={handleSendMessage}
                  disabled={isLoading || !inputMessage.trim()}
                  className="p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Send className="h-5 w-5" />
                </button>
              </div>
            </div>
          </>
        )}
        
        {/* Settings View */}
        {currentView === 'settings' && (
          <div className="flex-1 overflow-y-auto p-6">
            <div className="max-w-4xl mx-auto space-y-8">
              {/* API Configuration */}
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Settings className="h-5 w-5 mr-2" />
                  LLM API Configuration
                </h3>
                <div className="space-y-4">
                  {apiConfigs.map((config, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <h4 className="font-medium mb-3">{config.name}</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Endpoint URL
                          </label>
                          <input
                            type="text"
                            value={config.endpoint}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            readOnly
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            API Key
                          </label>
                          <input
                            type="password"
                            placeholder="Enter API key..."
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              {/* Data Training */}
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Database className="h-5 w-5 mr-2" />
                  Training Data Management
                </h3>
                <div className="space-y-4">
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                    <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                    <p className="text-gray-600 mb-4">Upload your enterprise documents and data</p>
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                      Choose Files
                    </button>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">0</div>
                      <div className="text-sm text-gray-600">Documents</div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">0 MB</div>
                      <div className="text-sm text-gray-600">Data Size</div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600">0</div>
                      <div className="text-sm text-gray-600">Training Jobs</div>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Security Settings */}
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Shield className="h-5 w-5 mr-2" />
                  Security & Privacy
                </h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium">Data Encryption</h4>
                      <p className="text-sm text-gray-600">Encrypt all data in transit and at rest</p>
                    </div>
                    <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                      Enabled
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium">Audit Logging</h4>
                      <p className="text-sm text-gray-600">Log all user interactions and system events</p>
                    </div>
                    <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                      Enabled
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium">Data Isolation</h4>
                      <p className="text-sm text-gray-600">Keep organization data completely isolated</p>
                    </div>
                    <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                      Enabled
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EnterpriseLLMApp;