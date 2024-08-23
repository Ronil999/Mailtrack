import { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth0 } from "@auth0/auth0-react";
import 'material-icons/iconfont/material-icons.css';

function Dashboard() {
  const { user, isAuthenticated, isLoading } = useAuth0();
  const [response, setResponse] = useState({ "data": { "res": [] } });
  const [bool, setBool] = useState(false);
  const [expandedRows, setExpandedRows] = useState([]);

  useEffect(() => {
    axios.post("https://mailtrack.vercel.app/dashdata", { "email": "ronillakhani999@gmail.com" })
      .then(res => {
        console.log("Backend Response:", res.data);
        setResponse(res.data);
        setBool(true);
      });
  }, []);

  const toggleRow = (index) => {
    if (expandedRows.includes(index)) {
      setExpandedRows(expandedRows.filter(i => i !== index));
    } else {
      setExpandedRows([...expandedRows, index]);
    }
  };

  const formatDateTime = (datetime) => {
    const [date, time] = datetime.split(' ');
    const [year, month, day] = date.split('-');
    const formattedDate = `${day}-${month}-${year}`;
    return { date: formattedDate, time };
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
        <div className="Firstline"></div>
        <div className="mails">
          <table cellSpacing="0" cellPadding="0">
            <thead>
              <tr>
                <th>From</th>
                <th>To</th>
                <th>Number of Times Opened</th>
                <th>Date</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {bool && response.res.map(({ opened, receiver, sender }, index) => {
                console.log("Opened Array:", opened);

                // Determine if the row should be expandable
                const isExpandable = opened && opened.length > 0;

                return (
                  <>
                    <tr key={index} 
                        onClick={() => isExpandable && toggleRow(index)} 
                        style={{ cursor: isExpandable ? 'pointer' : 'default' }}>
                      <td>{sender}</td>
                      <td>{receiver}</td>
                      <td>{opened ? opened.length : 0}</td>
                      <td></td> {/* Empty cell for date */}
                      <td></td> {/* Empty cell for time */}
                    </tr>

                    {isExpandable && expandedRows.includes(index) && (
                      <tr key={`${index}-details`}>
                        <td colSpan="5" style={{ backgroundColor: '#f9f9f9', padding: '10px' }}>
                          <table style={{ width: '100%' }}>
                            <thead>
                              <tr>
                                <th>Date</th>
                                <th>Time</th>
                              </tr>
                            </thead>
                            <tbody>
                              {opened.map((datetime, timeIndex) => {
                                const { date, time } = formatDateTime(datetime);
                                return (
                                  <tr key={timeIndex}>
                                    <td>{date}</td>
                                    <td>{time}</td>
                                  </tr>
                                );
                              })}
                            </tbody>
                          </table>
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
