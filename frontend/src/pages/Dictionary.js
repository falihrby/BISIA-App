import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Dictionary.css';

// Alphabet data (constant, moved outside the component)
const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

// Number data with keywords for Indonesian numbers (constant, moved outside the component)
const numbers = [
  { label: '1', src: '/angka/1.png', keywords: ['1', 'satu'] },
  { label: '2', src: '/angka/2.png', keywords: ['2', 'dua'] },
  { label: '3', src: '/angka/3.png', keywords: ['3', 'tiga'] },
  { label: '4', src: '/angka/4.png', keywords: ['4', 'empat'] },
  { label: '5', src: '/angka/5.png', keywords: ['5', 'lima'] },
  { label: '6', src: '/angka/6.png', keywords: ['6', 'enam'] },
  { label: '7', src: '/angka/7.png', keywords: ['7', 'tujuh'] },
  { label: '8', src: '/angka/8.png', keywords: ['8', 'delapan'] },
  { label: '9', src: '/angka/9.png', keywords: ['9', 'sembilan'] },
  { label: '10', src: '/angka/10.png', keywords: ['10', 'sepuluh'] },
  { label: '20', src: '/angka/20.png', keywords: ['20', 'dua puluh'] },
  { label: '100', src: '/angka/100.png', keywords: ['100', 'seratus'] },
  { label: '1000 (Cara ke-1)', src: '/angka/1000_1.png', keywords: ['1000', '1 seribu', 'seribu'] },
  { label: '1000 (Cara ke-2)', src: '/angka/1000_2.png', keywords: ['1000', '1 seribu', 'seribu'] },
  { label: '10.000 (Cara ke-1)', src: '/angka/10000_1.png', keywords: ['10.000', 'sepuluh ribu', '10 seribu'] },
  { label: '10.000 (Cara ke-2)', src: '/angka/10000_2.png', keywords: ['10.000', 'sepuluh ribu', '10 seribu'] },
  { label: '1 Juta', src: '/angka/1juta.png', keywords: ['satu juta', '1 juta'] },
  { label: '1 Miliar', src: '/angka/1miliar.png', keywords: ['satu miliar', '1 miliar'] },
  { label: '1 Triliun', src: '/angka/1triliun.png', keywords: ['satu triliun', '1 triliun'] },
];

// Default data combining alphabet and numbers (constant, moved outside the component)
const defaultData = [
  ...alphabet.map(letter => ({ label: letter, src: `/abjad/${letter}.png` })),
  ...numbers
];

function Dictionary() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [filteredData, setFilteredData] = useState([]);
  const [searchMessage, setSearchMessage] = useState('');

  // Utility function to determine if input is alphabetic
  const isAlphabet = input => /^[A-Za-z]+$/.test(input);

  // Utility function to determine if input is numeric
  const isNumberQuery = input => /\d/.test(input);

  // Utility function to match numbers with keywords and labels
  const matchNumber = (query, item) => {
    const normalizedQuery = query.toLowerCase().replace(/\s+/g, '').trim();
    const normalizedLabel = item.label.toLowerCase().replace(/\s+/g, '').trim();
    const matchesLabel = normalizedLabel === normalizedQuery;

    const matchesKeyword = item.keywords.some(keyword =>
      keyword.toLowerCase().replace(/\s+/g, '').includes(normalizedQuery)
    );

    return matchesLabel || matchesKeyword;
  };

  // Function to check if query contains invalid characters
  const containsInvalidCharacters = input => !/^[A-Za-z0-9\s]+$/.test(input);

  // Function to handle split query for letters like "Aku"
  const handleLetterSearch = (query) => {
    const letters = query.toUpperCase().split('');  // Split the query into individual letters
    const results = letters.map(letter => {
      return alphabet.includes(letter) ? { label: letter, src: `/abjad/${letter}.png` } : null;
    }).filter(result => result !== null);
    
    return results;
  };

  // Debounce function to delay execution
  const debounce = (func, delay) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func(...args), delay);
    };
  };

  // useEffect with an inline debounced search function
  useEffect(() => {
    const debouncedSearch = debounce(() => {
      if (searchQuery.trim() === '') {
        setFilteredData(defaultData);
        setSearchMessage('');
        setIsSearching(false);
        return;
      }

      setIsSearching(true);
      let filteredResults = [];

      if (containsInvalidCharacters(searchQuery)) {
        setFilteredData([]);
        setSearchMessage(`Tidak ada hasil ditemukan untuk ${searchQuery}`);
        return;
      }

      // Check for alphabetic search (split into letters)
      if (isAlphabet(searchQuery)) {
        filteredResults = handleLetterSearch(searchQuery);
      }
      // Check for numeric search
      else if (isNumberQuery(searchQuery)) {
        filteredResults = numbers.filter(number => matchNumber(searchQuery, number));
      }

      if (filteredResults.length === 0) {
        setSearchMessage(`Tidak ada hasil ditemukan untuk ${searchQuery}`);
      } else {
        setSearchMessage('');
      }

      setFilteredData(filteredResults);
    }, 300); // Delay of 300ms

    debouncedSearch();
    return () => clearTimeout(debouncedSearch); // Cleanup timeout on unmount
  }, [searchQuery]); // Only re-run when searchQuery changes

  return (
    <div className="content-wrapper">
      <section className="dictionary-bg-section text-center">
        <div className="overlay">
          <h3 className="text-white">Pelajari Bahasa Isyarat Huruf atau Angka Pilihanmu</h3>
          {/* Updated notification */}
          <p className="text-white">Untuk mencari lebih dari satu huruf, masukkan kata atau beberapa huruf tanpa spasi (misalnya "AKU")</p>
          <div className="my-4 input-group search-bar-wrapper">
            <input
              type="text"
              placeholder="Cari bahasa isyarat huruf atau angka..."
              className="form-control input-search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button className="btn btn-cari" onClick={() => setSearchQuery(searchQuery)}>
              Cari
            </button>
          </div>
        </div>
      </section>

      <div className="container kosakata-section">
        {isSearching && searchQuery && (
          <p className="kosakata-label">
            Hasil pencarian dari <strong>{searchQuery}</strong>
          </p>
        )}
      </div>

      <div className="container card-section">
        <div className="row">
          {filteredData.length > 0 ? (
            filteredData.map((item, index) => (
              <div key={index} className="col-md-3 col-sm-6 mb-4">
                <div className="card">
                  <img
                    src={item.src}
                    alt={`Item ${item.label}`}
                    className="card-image"
                  />
                  <p className="card-label">{item.label}</p>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center">
              <p>{searchMessage || 'Hasil pencarian tidak ditemukan.'}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dictionary;
