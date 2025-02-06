import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import * as d3 from 'd3';
import './App.css';

function App() {
  const [query, setQuery] = useState(''); // 用户输入的书名
  const [results, setResults] = useState([]); // 搜索结果
  const [loading, setLoading] = useState(false); // 加载状态
  const svgRef = useRef(null);

  // 处理搜索
  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:5001/search?book_name=${query}`);
      setResults(response.data);
    } catch (error) {
      console.error('搜索失败：', error);
    } finally {
      setLoading(false);
    }
  };

  // 处理书籍点击
  const handleBookClick = async (bookId) => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:5001/related_books?book_id=${bookId}`);
      console.log("Related Books Response:", response.data);
      drawGraph(response.data);
    } catch (error) {
      console.error('获取相关书籍失败：', error);
    } finally {
      setLoading(false);
    }
  };

  // 绘制力导向图
  const drawGraph = (data) => {
    const svg = d3.select(svgRef.current);
  
    // 清除之前的图表
    svg.selectAll('*').remove();
  
    const simulation = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.links).id(d => d.id))
      .force('charge', d3.forceManyBody().strength(-50))
      .force('center', d3.forceCenter(400, 300));
  
    // 绘制连接线
    const link = svg.append('g')
      .attr('stroke', '#000') // 设置为黑色
      .attr('stroke-opacity', 1.8) // 设置透明度为 0.8
      .attr('stroke-width', 2) // 设置宽度为 2
      .selectAll('line')
      .data(data.links)
      .enter().append('line')
      .on('mouseover', function(event, d) {
        d3.select(this).attr('stroke-width', 4); // 鼠标悬停时加粗
      })
      .on('mouseout', function(event, d) {
        d3.select(this).attr('stroke-width', 2); // 鼠标移出时恢复
      });
  
    // 绘制节点
    const node = svg.append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 2.5)
      .selectAll('circle')
      .data(data.nodes)
      .enter().append('circle')
      .attr('r', 10)
      .call(drag(simulation));
  
    // 添加节点上的书名
    const text = svg.append('g')
      .selectAll('text')
      .data(data.nodes)
      .enter().append('text')
      .attr('x', d => d.x)
      .attr('y', d => d.y)
      .attr('font-family', 'sans-serif')
      .attr('font-size', '10px')
      .attr('fill', 'black')
      .text(d => d.name);
  
    node.append('title')
      .text(d => d.description); // 添加鼠标悬停时显示的描述
  
    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
  
      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
  
      text
        .attr('x', d => d.x + 10)
        .attr('y', d => d.y + 5);
    });
  
    function drag(simulation) {
      function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }
  
      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }
  
      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
  
      return d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended);
    }
  };

  return (
    <div className="App">
      <h1>Book Chain</h1>
      <div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="输入书名"
        />
        <button onClick={handleSearch}>搜索</button>
      </div>
      <div>
        <h2>搜索结果</h2>
        {loading ? (
          <p>加载中...</p>
        ) : (
          <ul>
            {results.map((book) => (
              <li key={book.id} onClick={() => handleBookClick(book.id)}>
                <h3>{book.name}</h3>
                <p>{book.description}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
      <div>
        <h2>相关书籍</h2>
        <svg ref={svgRef} width="800" height="600"></svg>
      </div>
    </div>
  );
}

export default App;