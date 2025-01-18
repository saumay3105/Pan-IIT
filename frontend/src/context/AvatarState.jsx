import React, { createContext, useContext, useState } from 'react';

// Create the context
export const SpeakingContext = createContext();

// Create a provider component
export const SpeakingProvider = ({ children }) => {
    const [speaking, setSpeaking] = useState(false); // Default state

    return (
        <SpeakingContext.Provider value={{ speaking, setSpeaking }}>
            {children}
        </SpeakingContext.Provider>
    );
};
