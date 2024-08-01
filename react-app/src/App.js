import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';

function App() {
  const [renderTime, setRenderTime] = useState(null);

  useEffect(() => {
    const start = performance.now();

    // Simulate some work
    for (let i = 0; i < 1000000; i++) {
      Math.random();
    }

    const end = performance.now();
    const time = end - start;
    setRenderTime(time);

    // Log performance metrics to console
    console.log(`Render time: ${time.toFixed(2)} ms`);

    // Use Performance API to get more detailed metrics
    if (performance.getEntriesByType) {
      const perfEntries = performance.getEntriesByType('navigation');
      if (perfEntries.length > 0) {
        console.log('Navigation Timing:', perfEntries[0].toJSON());
      } else {
        console.log('Navigation timing data not available');
      }
    } else {
      console.log('Performance API not fully supported in this browser');
    }

    // Log React-specific performance metrics
    if (window.performance && performance.mark) {
      performance.mark('react-app-rendered');
      performance.measure('react-app-render-to-now', 'navigationStart', 'react-app-rendered');
      const measure = performance.getEntriesByName('react-app-render-to-now')[0];
      console.log(`Time since navigation start: ${measure.duration.toFixed(2)} ms`);
    }

  }, []);

  return (
    <div>
      <h1>React Performance Test</h1>
      {renderTime && <p>Render time: {renderTime.toFixed(2)} ms</p>}
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));

export default App