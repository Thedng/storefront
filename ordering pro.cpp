#include <iostream>
#include <string>
using namespace std;

int main()
{
    string inputData;
    getline(cin, inputData);
    
    if (inputData.length() < 5)
    {
        cout << "Error: Packet too short" << endl;
        return 1;
    }
    
    string headerData = inputData.substr(0, 4);
    
    char originID = headerData[0];
    char targetID = headerData[1];
    
    char statusFlags = headerData[2];
    bool syncFlag = statusFlags & 0b00000001;
    bool acknowledgeFlag = statusFlags & 0b00000010;
    bool priorityFlag = statusFlags & 0b10000000;
    
    int contentLength = static_cast<unsigned char>(headerData[3]) / 8;
    
    if (4 + contentLength >= inputData.length())
    {
        cout << "Error: Invalid payload length" << endl;
        return 1;
    }
    
    string mainContent = inputData.substr(4, contentLength);
    
    int wasteStartPos = contentLength + 4;
    int wasteLength = inputData.length() - contentLength - 5;
    string wasteContent = inputData.substr(wasteStartPos, wasteLength);
    
    int patternMatches = 0;
    for (int i = 0; i < contentLength - 1; i++)
    {
        if (mainContent[i] == '!' && mainContent[i + 1] == '?')
        {
            patternMatches++;
        }
    }
    
    char receivedVerification = inputData[inputData.length() - 1];
    char computedVerification = 0;
    
    for (int i = 0; i < contentLength; i++)
    {
        computedVerification ^= mainContent[i];
    }
    
    bool isCorrect = (receivedVerification == computedVerification);
    
    cout << "--- Packet Analysis ---" << endl;
    cout << "Source ID: " << originID << endl;
    cout << "Destination ID: " << targetID << endl;
    cout << "--- Flags ---" << endl;
    cout << "URGENT: " << (priorityFlag ? "Yes" : "No") << endl;
    cout << "ACK: " << (acknowledgeFlag ? "Yes" : "No") << endl;
    cout << "SYN: " << (syncFlag ? "Yes" : "No") << endl;
    cout << "Payload Length: " << contentLength << " bytes" << endl;
    cout << "Payload Data: " << mainContent << endl;
    cout << "Garbage Data: " << wasteContent << endl;
    cout << "\"!?\": Pattern Count: " << patternMatches << endl;
    cout << "--- Validation ---" << endl;
    cout << "Calculated Checksum: " << computedVerification << endl;
    cout << "Received Checksum: " << receivedVerification << endl;
    cout << "Result: " << (isCorrect ? "Packet is valid." : "Packet is invalid (checksum mismatch).") << endl;
    
    return 0;
}