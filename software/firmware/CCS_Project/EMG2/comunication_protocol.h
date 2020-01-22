



#include <stdint.h>

//// Structs ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Defines a structure type with a uint32_t parameter to be used by the comunication packet.

typedef struct {

    //Little-Endian Storage Structure

    uint16_t command       ;     // Byte[0-1] ; Size = 2 bytes ; Byte Offset = 0
    // Pad                 ;     // Byte[2-3] ; Size = 2 bytes ; Byte Offset = 2                 // 2 Bytes added after command for the structure have a size multiple of sizeof(uint32_t)
    uint32_t uint32_operand;     // Byte[4-7] ; Size = 4 bytes ; Byte Offset = 4

    //uint8_t  Chk_Sum_8bits 8;                                                                 // *One Byte is used for a CheckSum of the last 8 bits(Not yet implemented).

} uint32_parameter_packet;



// Defines a structure type with a float parameter to be used by the comunication packet.


typedef struct {

    uint16_t command       ;      // Byte[0-1] ; Size = 2 bytes ; Byte Offset = 0
    // Pad                 ;      // Byte[2-3] ; Size = 2 bytes ; Byte Offset = 2                 // 2 Bytes added after command for the structure have a size multiple of sizeof(uint32_t)
    float    float_operand ;      // Byte[4-7] ; Size = 4 bytes ; Byte Offset = 4

    //uint8_t Chk_Sum_8bits 8;                                                                   // *One Byte is used for a CheckSum of the last 8 bits(Not yet implemented).

} float_parameter_packet;




// Defines three perspectives for a packet: 1 - Packet with a uin32 operand; 2 - Packet with a float operand; 3 - uint32 vector.

typedef union{
        uint32_parameter_packet uint32_param_pkt;
        float_parameter_packet  float_param_pkt;
        uint8_t                 bytes[8];

} comunication_packet;


/// To be placed in another module in short future


typedef struct {

    uint32_t timestamp         ;
    uint32_t period_Func_Gen   ;    // Byte[x-x] ; Size =   bytes ; Byte Offset =
    uint8_t  wave_form         ;
    uint32_t func_gen_frequence;


} tiva_status;

#define ADC_ACQUISITION         0
#define FUNC_GEN_ACQUISITION    1

/// End of "To be placed in another module in short future"


//// Constants ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Commands to be interpreted by the command handler
//
// ASCII Dictionary
//
// a = 0x61
// b = 0x62
// c = 0x63
// f = 0x66
// g = 0x67
// i = 0x69
// k = 0x6b
// n = 0x6E
// o = 0x6f
// p = 0x70
// q = 0x71
// r = 0x72
// s = 0x73
// w = 0x77

#define START_TRANSMISSION           0x6169  //  "ai"
#define STOP_TRANSMISSION            0x6173  //  "as"

#define SET_SAMPLE_RATE             0x7372  //  "sr"
#define SET_NUMBER_CHANNELS         0x7363  //  "sc"
#define SET_NUMBER_BOARDS           0x7362  //  "sb"
#define SET_NUMBER_BYTES_IN_PACKET  0x7370  //  "sp"
#define SET_BITS_PER_SAMPLE         0x7373  //  "ss"
#define SET_ADC_ACQUISITION         0x6661  //  "fa"

#define GET_SAMPLE_RATE             0x6772  //  "gr"
#define GET_NUMBER_CHANNELS         0x6763  //  "gc"
#define GET_NUMBER_BOARDS           0x6762  //  "gb"
#define GET_NUMBER_BYTES_IN_PACKET  0x6770  //  "gp"
#define GET_BITS_PER_SAMPLE         0x6773  //  "gs"

#define ACK                         0x6f6b  //  "ok"
#define NAK                         0x6e6b  //  "nk"

// Function Generator Commands

#define SET_FUNC_GEN_FREQUENCE      0x7366  //  "sf"
#define SET_FUNC_GEN_SQUARE_WAVE    0x6671  //  "fq"
#define SET_FUNC_GEN_SAWTOOTH_WAVE  0x6677  //  "fw"
#define SET_FUNC_GEN_SIN_WAVE       0x666E  //  "fn"

#define GET_FUNC_GEN_WAVE_FORM      0x6766  //  "gf"



// Properties ofcomunication_packet: Offset and Size in Bytes.

#define OFFSET_COMMAND              0
#define OFFSET_OPERAND              4

#define SIZE_COMMAND                2
#define SIZE_OPERAND                4

//

#define LENGTH_BUFFER_IN           64
#define LENGTH_BUFFER_OUT          64



// functions prototypes

void command_handler (comunication_packet *pkt_received, tiva_status *tiva_actual_state );
void send_packet     (comunication_packet *pkt_to_send                                  );
void recieve_packet  (comunication_packet *pkt_to_be_received                           );
void stop_trasmission(                                                                  );
