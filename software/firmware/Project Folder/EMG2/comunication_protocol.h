



#include <stdint.h>
#include <string.h>
#include "tiva_HAL.h"

//// Structs ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Defines a structure type with a uint32_t parameter to be used by the communication packet.

typedef struct {

    //Little-Endian Storage Structure

    uint16_t command       ;     // Byte[0-1] ; Size = 2 bytes ; Byte Offset = 0
    // Padding             ;     // Byte[2-3] ; Size = 2 bytes ; Byte Offset = 2                 // 2 Bytes added after "command" for the address of "uint32_operand" be a multiple of 4(bytes).
    uint32_t uint32_operand;     // Byte[4-7] ; Size = 4 bytes ; Byte Offset = 4

    //uint8_t  Chk_Sum_8bits 8;                                                                 // *One Byte is used for a CheckSum of the last 8 bits(Not yet implemented).

} uint32_parameter_packet;



// Defines a structure type with a float32 parameter to be used by the communication packet.


typedef struct {

    uint16_t command       ;      // Byte[0-1] ; Size = 2 bytes ; Byte Offset = 0
    // Padding             ;      // Byte[2-3] ; Size = 2 bytes ; Byte Offset = 2                // 2 Bytes added after "command" for the address of "float_operand" be a multiple of 4(bytes).
    float    float_operand ;      // Byte[4-7] ; Size = 4 bytes ; Byte Offset = 4

    //uint8_t Chk_Sum_8bits 8;                                                                   // *One Byte is used for a CheckSum of the last 8 bits(Not yet implemented).

} float_parameter_packet;




// Defines three perspectives for a packet: 1 - Packet with a uin32 operand; 2 - Packet with a float operand; 3 - uint32 vector.

typedef union{
        uint32_parameter_packet uint32_param_pkt;
        float_parameter_packet  float_param_pkt;
        uint8_t                 bytes[8];

} comunication_packet;





//// Constants ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Commands to be interpreted by the command handler
//
// ASCII Dictionary
//
// a = 0x61
// b = 0x62
// c = 0x63
// e = 0x65
// f = 0x66
// g = 0x67
// i = 0x69
// k = 0x6b
// m = 0x6d
// n = 0x6E
// o = 0x6f
// p = 0x70
// q = 0x71
// r = 0x72
// s = 0x73
// u = 0x75
// v = 0x76
// w = 0x77

#define START_TRANSMISSION          0x6169  //  "ai"
#define STOP_TRANSMISSION           0x6173  //  "as"

#define SET_TRANSMISSION_MODE       0x736d  //  "sm"
#define SET_SAMPLE_RATE             0x7372  //  "sr"
#define SET_NUMBER_CHANNELS         0x7363  //  "sc"
#define SET_NUMBER_BOARDS           0x7362  //  "sb"
#define SET_NUMBER_BYTES_IN_PACKET  0x7370  //  "sp"
#define SET_BITS_PER_SAMPLE         0x7373  //  "ss"
#define SET_ADC_ACQUISITION         0x6661  //  "fa"

#define GET_TRANSMISSION_MODE       0x676d  //  "gm"
#define GET_SAMPLE_RATE             0x6772  //  "gr"
#define GET_NUMBER_CHANNELS         0x6763  //  "gc"
#define GET_NUMBER_BOARDS           0x6762  //  "gb"
#define GET_NUMBER_BYTES_IN_PACKET  0x6770  //  "gp"
#define GET_BITS_PER_SAMPLE         0x6773  //  "gs"

#define ACK                         0x6f6b  //  "ok"
#define NAK                         0x6d65  //  "me"


// Return Types

#define INT32_VALUE                 0x7675  //  "vu"
#define FLOAT32_VALUE               0x7666  //  "vf"
#define STREAMING_PKT               0x6d73  //  "ms"
#define ERROR_MSG                   0x6d65  //  "me"
#define WARNING_MSG                 0X6d77  //  "mw"


// Function Generator Commands

#define SET_FUNC_GEN_FREQUENCY      0x7366  //  "sf"
#define SET_FUNC_GEN_SQUARE_WAVE    0x6671  //  "fq"
#define SET_FUNC_GEN_SAWTOOTH_WAVE  0x6677  //  "fw"
#define SET_FUNC_GEN_SIN_WAVE       0x666E  //  "fn"

#define GET_FUNC_GEN_WAVE_FORM      0x6777  //  "gw"
#define GET_FUNC_GEN_FREQUENCY      0x6766  //  "gf"



// Error Messages

// Out of Range

#define MSG_OOR_FUNC_GEN_FREQUENCY   " Hz it is Outside the Range Accepted by the Function Generator.\nTry a Value bigger than 0 and less than SampleRate / 2.\nFor the Current Configuration, Please use a value between: \0"
#define MSG_OOR_SAMPLE_RATE          " Hz of Sample Rate it is Outside the Range Accepted by the Board.\nTry a Value bigger than 0 and less or equal than 1MHZ / (Total Number of Channels).\nFor the Current Configuration, Please use a value between: \0"
#define MSG_OOR_NUMBER_CHANNELS      " Channel(s) it out of the Outside the Range Accepted by the Board.\nPlease use a value between: \0"
#define MSG_OOR_NUMBER_BOARDS        " Acquisition Board(s) it is Outside the Range Accepted by the Board.\nPlease use a value between: \0"
#define MSG_OOR_BYTES_IN_PACKET      " Byte(s) in a Packet it is Outside the Range Accepted by the Board.\nFor the current settings. Please use a value between: \0"
#define MSG_OOR_BITS_PER_SAMPLE      " bits per Sample it is Outside the Range Accepted by the Board.\nPlease use a value between: \0"

// Types of Acquisition

#define MSG_UKN_TYPE_OF_ACQUISIION   "The Board do not Recognize this Acquisition Mode."


// Types of Transmission Mode

#define MSG_UKN_TRANSMISSION_MODE    "The Board do not Recognize this Transmission Mode."


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

uint32_t msg_generator( uint32_t value, char* default_msg, uint32_t start_range, uint32_t end_range, char* out_msg );
// Macros

//# define MSG_OOR_BITS_PER_SAMPLE ()

