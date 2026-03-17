import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { fetchAgingSummary } from '../api';

const COLORS = ['#22c55e', '#eab308', '#f97316', '#ef4444'];

function AgingChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchAgingSummary()
      .then((resp) => {
        const raw = resp.data;
        setData([
          { bucket: '0-30d', count: raw['0-30'] },
          { bucket: '31-60d', count: raw['31-60'] },
          { bucket: '61-90d', count: raw['61-90'] },
          { bucket: '90+d', count: raw['90+'] },
        ]);
      })
      .catch(() => setData([]));
  }, []);

  return (
    <div className="aging-chart">
      <h3 className="chart-title">Claims by Aging Bucket</h3>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#21262d" />
          <XAxis dataKey="bucket" stroke="#8b949e" fontSize={12} />
          <YAxis stroke="#8b949e" fontSize={12} />
          <Tooltip
            contentStyle={{ background: '#161b22', border: '1px solid #21262d', borderRadius: 6, color: '#e1e4e8' }}
          />
          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default AgingChart;
