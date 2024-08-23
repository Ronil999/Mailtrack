import { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth0 } from "@auth0/auth0-react";
import 'material-icons/iconfont/material-icons.css';

function Dashboard() {
  const { user, isAuthenticated, isLoading } = useAuth0();
  const [response, setResponse] = useState({ "data": { "res": [] } });
  const [bool, setBool] = useState(false);
  const [expandedRows, setExpandedRows] = useState([]); // State to track expanded rows

  useEffect(() => {
    axios.post("https://mailtrack.vercel.app/dashdata",
      { "email": "ronillakhani999@gmail.com" }
    )
      .then(res => {
        console.log(res);
        console.log(res.data);
        setResponse(res.data);
        setBool(true);
      });
  }, []);

  const toggleRow = (index) => {
    // Toggle expanded rows
    setExpandedRows(expandedRows.includes(index)
      ? expandedRows.filter(i => i !== index)
      : [...expandedRows, index]);
  };

  const splitOpenedString = (opened) => {
    // Split the string into chunks of 19 characters if needed
    if (typeof opened === 'string' && opened.length > 0) {
      return opened.match(/.{19}/g) || []; // Split every 19 characters
    }
    return opened; // If opened is already an array, return as-is
  };

  return (
    <div className="dashboard">
      <div className="sendmail">
        <div>
          <a href="send">Send Mail</a>
          <span className="material-icons-round">send</span>
        </div>
      </div>
      <h1>Dashboard</h1>
      <div className="DashboardContents">
        <div className="Firstline">
        </div>
        <div className="mails">
          <table cellSpacing="0" cellPadding="0">
            <tbody>
              <tr>
                <th>From</th>
                <th>To</th>
                <th>Number of Times Opened</th>
              </tr>
              
              {bool && response.res.map(({ opened, receiver, sender }, index) => {
                // Ensure `opened` is an array
                let openedArray = Array.isArray(opened) ? opened : splitOpenedString(opened);

                return (
                  <>
                    {/* Render the main row */}
                    <tr key={index} 
                        onClick={() => openedArray.length > 0 && toggleRow(index)} 
                        style={{ cursor: openedArray.length > 0 ? 'pointer' : 'default' }}>
                      <td>{sender}</td>
                      <td>{receiver}</td>
                      <td>{openedArray.length}</td>
                    </tr>

                    {/* Conditionally render the expanded row only if `openedArray.length > 0` and row is expanded */}
                    {openedArray.length > 0 && expandedRows.includes(index) && (
                      <tr key={`${index}-details`}>
                        <td colSpan="3" style={{ backgroundColor: '#f9f9f9', padding: '10px' }}>
                          <ul style={{ listStyleType: 'none', padding: 0, margin: 0 }}>
                            {openedArray.map((time, timeIndex) => (
                              <li key={timeIndex} style={{ marginBottom: '5px', color: '#000' }}>
                                {time}
                              </li>
                            ))}
                          </ul>
                        </td>
                      </tr>
                    )}
                  </>
                );
              })}
              
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
