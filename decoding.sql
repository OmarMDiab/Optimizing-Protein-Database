-- Example SQL function to decode a
-- DNA sequence
CREATE OR REPLACE FUNCTION decode_dna
  (encoded_sequence BYTEA) RETURNS TEXT AS $$
DECLARE
  result TEXT := '';
  nucleotide TEXT;
  byte_val INTEGER;
BEGIN
  FOR i IN 0..octet_length(encoded_sequence)
              - 1
  LOOP
    -- Extract each byte from the encoded
    -- sequence
    byte_val := get_byte(encoded_sequence, i);
    -- Decode each byte to the corresponding
    -- nucleotide and append to the result
    nucleotide := (
      CASE byte_val
        WHEN 0 THEN 'A'
        WHEN 1 THEN 'C'
        WHEN 2 THEN 'G'
        WHEN 3 THEN 'T'
      END
    );
    result := result || nucleotide;
  END LOOP;
  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Example usage
SELECT decode_dna(encoded_sequence)
FROM dna_sequences WHERE id = 1;